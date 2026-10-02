"""登记、辞例、领号、反证与试点日志的校验。"""

from __future__ import annotations

import csv
import json
import re
import unicodedata
from datetime import datetime, timedelta, timezone
from difflib import ndiff
from pathlib import Path
from urllib.parse import urlparse

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
ID_RE = re.compile(r"^OBD-\d{6}$")
OBD_TOKEN_RE = re.compile(r"〔OBD-\d{6}〕")
URL_RE = re.compile(r"https?://[^\s)>\]]+")
IMAGE_RE = re.compile(
    r"(?i)(?:^|[\s'\"“])([^\s'\"“]+\.(?:png|jpe?g|gif|webp|svg|tiff?|bmp))(?:$|[\s'\"”])"
)
DATA_IMAGE_RE = re.compile(r"(?i)data:image/")
HAN_RANGES = (
    (0x3400, 0x4DBF),
    (0x4E00, 0x9FFF),
    (0x20000, 0x2A6DF),
    (0x2A700, 0x2B73F),
    (0x2B740, 0x2B81F),
    (0x2B820, 0x2CEAF),
    (0x2CEB0, 0x2EBEF),
    (0x30000, 0x3134F),
)
ALLOWED_SYMBOLS = set("□…【】{}々?〔〕")
IDS_RANGE = (0x2FF0, 0x2FFF)
BRACKET_PAIRS = {"【": "】", "{": "}", "〔": "〕"}
CITATION_MARKERS_FALLBACK = ("未识", "未释", "存疑", "undeciphered", "doubtful")
FORBIDDEN_STATUS_WORDS = ("已破译", "已确认", "已有定论", "定论")
SUBSTANTIVE_KINDS = {
    "reading_fails_in_context",
    "source_mismatch",
    "previously_proposed_and_rejected",
}
PILOT_LEVELS = (
    "证据不足暂不结论",
    "线索待查",
    "候选假说",
    "候选假说有争议",
    "已被排除",
)
PILOT_LEVEL_RANK = {name: index for index, name in enumerate(PILOT_LEVELS)}
# 无检索范围时，最高只能到“线索待查”；排除与候选假说都更高。
PILOT_SCOPE_CEILING = "线索待查"
HYPOTHESIS_LEVELS = {"候选假说", "候选假说有争议"}
PILOT_HEADINGS = (
    "## 证据清单",
    "## 已排除的假说",
    "## 反证与回应",
    "## AI 线索",
    "## 当前结论与升级条件",
    "## 变更说明",
)
PROPOSAL_REQUIRED_IDS = (
    "glyph_id",
    "evolution_chain",
    "inscriptions",
    "references",
    "argument",
    "relation_to_prior",
    "source_citation",
)
ISSUE_FORMS = {
    ".github/ISSUE_TEMPLATE/decipherment-proposal.yml": PROPOSAL_REQUIRED_IDS,
    ".github/ISSUE_TEMPLATE/glyph-registration.yml": (
        "glyph_id",
        "catalog_ref",
        "problem",
    ),
    ".github/ISSUE_TEMPLATE/data-source.yml": ("name", "url", "license_note"),
    ".github/ISSUE_TEMPLATE/request-glyph-id.yml": ("source", "description"),
}


def load_policy(root: Path | None = None) -> dict:
    root = root or ROOT
    return json.loads((root / "registry" / "policy.json").read_text(encoding="utf-8"))


def schema_validator(root: Path, relative: str) -> Draft202012Validator:
    schema = json.loads((root / relative).read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def schema_errors(validator: Draft202012Validator, instance: object, label: str) -> list[str]:
    messages = []
    for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path)):
        path = "/".join(str(part) for part in error.path) or "(root)"
        messages.append(f"{label}: {path}: {error.message}")
    return messages


def read_yaml(path: Path) -> object:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def iter_yaml(directory: Path) -> list[tuple[Path, object]]:
    if not directory.exists():
        return []
    rows = []
    for path in sorted(directory.rglob("*.yaml")):
        rows.append((path, read_yaml(path)))
    return rows


def load_domain_allowlist(root: Path) -> set[str]:
    text = (root / "registry" / "allowed-link-domains.txt").read_text(encoding="utf-8")
    domains = set()
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip().lower()
        if line:
            domains.add(line)
    return domains


def load_normalize_table(root: Path) -> list[tuple[str, str]]:
    path = root / "data" / "normalize.csv"
    pairs: list[tuple[str, str]] = []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        expected = ["source_char", "normalized_char", "note"]
        if reader.fieldnames != expected:
            raise ValueError(
                "data/normalize.csv 表头必须是 source_char,normalized_char,note"
            )
        for row in reader:
            source = (row.get("source_char") or "").strip()
            target = (row.get("normalized_char") or "").strip()
            if not source or source.startswith("#"):
                continue
            pairs.append((source, target))
    pairs.sort(key=lambda item: len(item[0]), reverse=True)
    return pairs


def normalize_transcription(text: str, table: list[tuple[str, str]]) -> str:
    for source, target in table:
        text = text.replace(source, target)
    return unicodedata.normalize("NFC", text)


def _is_han(character: str) -> bool:
    code = ord(character)
    return any(start <= code <= end for start, end in HAN_RANGES)


def transcription_errors(
    entry: dict,
    table: list[tuple[str, str]],
    policy: dict,
    label: str,
) -> list[str]:
    errors: list[str] = []
    raw = entry.get("transcription")
    if not isinstance(raw, str):
        return errors
    if "\n" in raw or "\r" in raw:
        errors.append(f"{label}: transcription 必须是单行")
    text = normalize_transcription(raw, table)
    if any(IDS_RANGE[0] <= ord(char) <= IDS_RANGE[1] for char in text):
        errors.append(f"{label}: transcription 不得使用 IDS；无 Unicode 的字形写成〔OBD-xxxxxx〕")
    without_tokens = OBD_TOKEN_RE.sub("", text)
    if "〔" in without_tokens or "〕" in without_tokens:
        errors.append(f"{label}: 〔〕只能用于〔OBD-六位编号〕")
    for character in without_tokens:
        if _is_han(character) or character in ALLOWED_SYMBOLS:
            continue
        errors.append(f"{label}: transcription 含未允许字符 {character!r}")
        break
    stack: list[str] = []
    for character in text:
        if character in BRACKET_PAIRS:
            stack.append(character)
        elif character in BRACKET_PAIRS.values():
            if not stack or BRACKET_PAIRS[stack[-1]] != character:
                errors.append(f"{label}: 括号不成对")
                stack = []
                break
            stack.pop()
    if stack:
        errors.append(f"{label}: 括号不成对")
    damage = entry.get("damage_level")
    box_count = text.count("□")
    has_ellipsis = "…" in text
    has_restoration = "【" in text
    minor_max = int(policy["minor_box_max"])
    if damage == "complete" and (box_count or has_ellipsis or has_restoration):
        errors.append(f"{label}: damage_level 为 complete 时不得出现 □、… 或推补")
    if has_restoration and damage == "complete":
        errors.append(f"{label}: 出现推补时 damage_level 不得为 complete")
    if damage == "minor" and (has_ellipsis or box_count > minor_max):
        errors.append(
            f"{label}: minor 与缺字标记矛盾（□ 超过 {minor_max} 或含 …；该上限为经验设定，待校准）"
        )
    if damage == "severe" and box_count == 0 and not has_ellipsis:
        errors.append(f"{label}: severe 须含 □ 或 …")
    if "々" in text and not str(entry.get("note") or "").strip():
        errors.append(f"{label}: 使用々时必须在 note 中展开原字")
    return errors


def pointer_errors(value: object, allowlist: set[str], label: str) -> list[str]:
    errors: list[str] = []

    def walk(node: object, path: str) -> None:
        if isinstance(node, dict):
            for key, item in node.items():
                walk(item, f"{path}.{key}")
        elif isinstance(node, list):
            for index, item in enumerate(node):
                walk(item, f"{path}[{index}]")
        elif isinstance(node, str):
            if DATA_IMAGE_RE.search(node) or IMAGE_RE.search(f" {node} "):
                errors.append(f"{label}: {path} 含图像文件或图像链接，起步数据只允许指针")
            for match in URL_RE.findall(node):
                host = urlparse(match).hostname or ""
                host = host.lower()
                if host not in allowlist:
                    errors.append(f"{label}: {path} 的外链域名未登记: {host}")

    walk(value, label)
    return errors


def citation_ok(text: str, policy: dict) -> bool:
    markers = tuple(policy.get("source_citation_markers") or CITATION_MARKERS_FALLBACK)
    return any(marker in text for marker in markers)


def parse_date(value: str) -> datetime:
    text = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def abandon_stale(ledger: dict, now: datetime, abandon_days: int) -> list[str]:
    """把超期未使用的 pending 编号标为废弃。编号不删除。返回被标记的 ID。"""
    changed = []
    for row in ledger.get("allocations", []):
        if row.get("state") != "pending":
            continue
        issued = parse_date(row["issued_at"])
        if now - issued > timedelta(days=abandon_days):
            row["state"] = "abandoned"
            changed.append(row["glyph_id"])
    return changed


def is_reserved_test_id(glyph_id: str, policy: dict) -> bool:
    """OBD-900001 至 OBD-900099 只给演练，永不发给真实字形。"""
    if not glyph_id or not ID_RE.match(glyph_id):
        return False
    number = int(glyph_id.split("-")[1])
    low = int(policy["reserved_test_id_min"])
    high = int(policy["reserved_test_id_max"])
    return low <= number <= high


def next_glyph_id(ledger: dict, policy: dict) -> str:
    numbers = []
    for row in ledger.get("allocations", []):
        glyph_id = row["glyph_id"]
        if not ID_RE.match(glyph_id):
            continue
        numbers.append(int(glyph_id.split("-")[1]))
    nxt = (max(numbers) + 1) if numbers else 1
    low = int(policy["reserved_test_id_min"])
    high = int(policy["reserved_test_id_max"])
    while low <= nxt <= high:
        nxt += 1
    if nxt > 999999:
        raise ValueError("编号空间已用尽")
    glyph_id = f"OBD-{nxt:06d}"
    if is_reserved_test_id(glyph_id, policy):
        raise ValueError(f"拒绝发出测试编号 {glyph_id}")
    return glyph_id


def allocate_id(
    ledger: dict,
    account: str,
    description: str,
    source_note: str,
    now: datetime,
    policy: dict,
) -> dict:
    abandon_stale(ledger, now, int(policy["pending_id_abandon_days"]))
    pending = [
        row
        for row in ledger["allocations"]
        if row["state"] == "pending" and row["issued_to"] == account
    ]
    cap = int(policy["pending_id_cap_per_account"])
    if len(pending) >= cap:
        raise ValueError(
            f"{account} 挂起未录入编号已达 {cap}（经验设定，待校准），不能再领号"
        )
    glyph_id = next_glyph_id(ledger, policy)
    row = {
        "glyph_id": glyph_id,
        "issued_to": account,
        "issued_at": now.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "state": "pending",
        "source_note": source_note,
        "description": description,
        "duplicate_checked_by": "",
    }
    ledger["allocations"].append(row)
    return row


def ledger_errors(ledger: dict, policy: dict, now: datetime) -> list[str]:
    errors = []
    seen: set[str] = set()
    pending_counts: dict[str, int] = {}
    abandon_days = int(policy["pending_id_abandon_days"])
    cap = int(policy["pending_id_cap_per_account"])
    for index, row in enumerate(ledger.get("allocations", [])):
        label = f"id-ledger[{index}]"
        glyph_id = row.get("glyph_id", "")
        if is_reserved_test_id(glyph_id, policy):
            errors.append(
                f"{label}: 测试编号段永不发给真实字形 {glyph_id}"
            )
        if glyph_id in seen:
            errors.append(f"{label}: 编号重复，发出的编号不得复用 {glyph_id}")
        seen.add(glyph_id)
        state = row.get("state")
        if state == "used" and not str(row.get("duplicate_checked_by") or "").strip():
            errors.append(f"{label}: 已使用编号缺少复核者去重确认")
        if state == "pending":
            account = row.get("issued_to", "")
            pending_counts[account] = pending_counts.get(account, 0) + 1
            issued = parse_date(row["issued_at"])
            if now - issued > timedelta(days=abandon_days):
                errors.append(
                    f"{label}: 超过 {abandon_days} 天未使用，必须标为废弃而不是继续挂起"
                )
    for account, count in pending_counts.items():
        if count > cap:
            errors.append(f"id-ledger: {account} 挂起编号 {count} 超过上限 {cap}")
    return errors


def evidence_errors(record: dict, label: str) -> list[str]:
    errors = []
    for index, item in enumerate(record.get("evidence") or []):
        if not isinstance(item, dict):
            errors.append(f"{label}: evidence[{index}] 不是对象")
            continue
        if "candidate_id" in item or item.get("kind") in {"ai", "machine-suggestion"}:
            errors.append(f"{label}: 证据字段不得引用机器候选")
        blob = json.dumps(item, ensure_ascii=False)
        if "machine-suggestion" in blob or "cand-" in blob:
            errors.append(f"{label}: 证据字段不得引用机器候选")
    return errors


def accounts_related(left: str, left_links: list[str], right: str, right_links: list[str]) -> bool:
    left_set = {left, *left_links}
    right_set = {right, *right_links}
    return bool(left_set & right_set)


def classify_counterexample(item: dict) -> str:
    required = ("catalog_ref", "quotation", "conflict_with", "why", "verifiable_source")
    if any(not str(item.get(key) or "").strip() for key in required):
        return "unformed"
    kind = item.get("kind")
    if kind not in SUBSTANTIVE_KINDS:
        return "unformed"
    if kind == "previously_proposed_and_rejected" and not str(item.get("page") or "").strip():
        return "unformed"
    return "substantive"


def counterexample_account_errors(items: list[dict], policy: dict) -> list[str]:
    errors = []
    cap = int(policy["unformed_counterexample_cap_per_proposal"])
    counts: dict[str, int] = {}
    for item in items:
        if classify_counterexample(item) != "unformed":
            continue
        author = str(item.get("author") or "")
        counts[author] = counts.get(author, 0) + 1
    for author, count in counts.items():
        if author and count > cap:
            errors.append(
                f"反例: {author} 对同一提案的未成形反例超过 {cap}（经验设定，待校准）"
            )
    return errors


def suspension_due(rejected_count: int, policy: dict) -> bool:
    return rejected_count >= int(policy["rejected_counterexample_suspension_count"])


def review_errors(record: dict, policy: dict, today: datetime) -> list[str]:
    errors = []
    label = record.get("glyph_id", "record")
    status = record.get("review_status")
    tier = record.get("status_tier")
    if tier not in policy["status_tiers_allowed_first_batch"]:
        errors.append(f"{label}: 第一批校验不放行 status_tier={tier}")
    if any(word in str(status) for word in FORBIDDEN_STATUS_WORDS):
        errors.append(f"{label}: 不得使用“已破译/已确认/已有定论”等状态")
    if status == "专家认可" or not policy.get("expert_endorsement_enabled", False):
        if status == "专家认可":
            errors.append(f"{label}: “专家认可”暂空置，待有专业评审者加入后启用")
    verification = record.get("verification") or {}
    locked = bool(verification.get("locked"))
    proposer = record.get("proposer")
    if locked:
        reviewer = verification.get("reviewer")
        if reviewer == proposer or not reviewer:
            errors.append(f"{label}: 形式门锁定必须由提案人以外的复核者完成")
        if verification.get("checked_against_catalog") is not True:
            errors.append(f"{label}: 锁定前必须对照著录号复核")
    if status in {"可接受的候选", "专家认可"} and not locked:
        errors.append(f"{label}: 辞例数与残缺程度尚未锁定，提案人自填不生效")
    if status == "可接受的候选":
        disclaimer = policy["acceptable_candidate_disclaimer"]
        if record.get("disclaimer") != disclaimer:
            errors.append(f"{label}: 可接受的候选必须标注固定声明：{disclaimer}")
        if not verification.get("all_attestations_read"):
            errors.append(f"{label}: 通读无遗漏尚未被锁定确认")
        count = verification.get("attestation_count")
        damage = verification.get("damage_level")
        # 上限规则阻止的是高于“可接受的候选”。本档本身允许少辞例或重残。
        reviewers = record.get("community_reviewers") or []
        confirmed = [
            item
            for item in reviewers
            if item.get("confirmed_citations") and item.get("confirmed_complete_reading")
        ]
        need = int(policy["minimum_community_reviewers"])
        if len(confirmed) < need:
            errors.append(f"{label}: 可接受的候选需要至少 {need} 名社区复核者独立确认")
        logins = [item.get("login") for item in confirmed]
        if len(set(logins)) != len(logins):
            errors.append(f"{label}: 复核者账号重复")
        for index, left in enumerate(confirmed):
            if accounts_related(
                left.get("login", ""),
                left.get("linked_accounts") or [],
                proposer,
                [],
            ):
                errors.append(f"{label}: 复核者与提案人或其关联账号重合，须回避")
            for right in confirmed[index + 1 :]:
                if accounts_related(
                    left.get("login", ""),
                    left.get("linked_accounts") or [],
                    right.get("login", ""),
                    right.get("linked_accounts") or [],
                ):
                    errors.append(f"{label}: 两名复核者并非互不相关")
        counter = record.get("counterevidence") or {}
        if counter.get("open"):
            errors.append(f"{label}: 反证期尚未结束，不能进入可接受的候选")
        for item in counter.get("items") or []:
            if classify_counterexample(item) != "substantive":
                continue
            response = item.get("response")
            created = item.get("created_on")
            if created:
                due = parse_date(created) + timedelta(days=int(policy["response_days"]))
                if response is None and today > due:
                    errors.append(f"{label}: 实质反例逾期未回应，不得进入可接受的候选")
            if not response:
                errors.append(f"{label}: 存在未回应的实质反例")
            upheld = item.get("upheld_by") or []
            blocked = {proposer, item.get("author")}
            independent = [name for name in upheld if name and name not in blocked]
            if len(set(independent)) >= 2:
                errors.append(f"{label}: 已成立的反例须退回“有争议”")
        _ = count, damage
    if status == "专家认可":
        count = (verification or {}).get("attestation_count")
        damage = (verification or {}).get("damage_level")
        ceiling = int(policy["attestation_count_ceiling"])
        if isinstance(count, int) and count <= ceiling:
            errors.append(
                f"{label}: 锁定后的辞例数 ≤ {ceiling}，状态不得超过可接受的候选"
            )
        if damage == policy["severe_damage"]:
            errors.append(f"{label}: 存在重残，状态不得超过可接受的候选")
    votes = record.get("priority_votes") or []
    for vote in votes:
        if isinstance(vote, dict) and vote.get("affects_status") is not False:
            errors.append(f"{label}: 社区票不能改变状态")
    errors.extend(evidence_errors(record, label))
    errors.extend(
        counterexample_account_errors(
            (record.get("counterevidence") or {}).get("items") or [],
            policy,
        )
    )
    return errors


def severe_attestation_present(entries: list[dict]) -> bool:
    return any(entry.get("damage_level") == "severe" for entry in entries)


def status_ceiling_blocks_endorsement(record: dict, entries: list[dict], policy: dict) -> list[str]:
    """锁定值或辞例中的重残，使状态不能高于可接受的候选。"""
    if record.get("review_status") != "专家认可":
        return []
    errors = []
    verification = record.get("verification") or {}
    if verification.get("locked"):
        count = verification.get("attestation_count")
        if isinstance(count, int) and count <= int(policy["attestation_count_ceiling"]):
            errors.append("状态封顶: 辞例数不足，不能高于可接受的候选")
        if verification.get("damage_level") == policy["severe_damage"]:
            errors.append("状态封顶: 锁定残缺程度为 severe")
    if severe_attestation_present(entries):
        errors.append("状态封顶: 辞例中存在 severe")
    return errors


def dual_report(left: dict, right: dict, table: list[tuple[str, str]]) -> dict:
    conflicts = []
    for field in ("glyph_id", "catalog_ref", "period_group", "damage_level", "source_citation"):
        if left.get(field) != right.get(field):
            conflicts.append(
                {
                    "field": field,
                    "left": left.get(field),
                    "right": right.get(field),
                }
            )
    a = normalize_transcription(str(left.get("transcription") or ""), table)
    b = normalize_transcription(str(right.get("transcription") or ""), table)
    symbol_diff = []
    if a != b:
        for line in ndiff(list(a), list(b)):
            if line.startswith(("- ", "+ ", "? ")):
                symbol_diff.append(line)
        conflicts.append({"field": "transcription", "symbol_diff": symbol_diff})
    same_person = left.get("entered_by") == right.get("entered_by")
    return {
        "consistent": not conflicts and not same_person,
        "conflicts": conflicts,
        "same_person": same_person,
        "auto_merge": False,
    }


def qualification_for(pairs: list[dict], login: str, policy: dict) -> dict:
    """一致率只回答某人是否够格做复核者，不产生排名。"""
    participated = 0
    consistent = 0
    for pair in pairs:
        people = {pair.get("left_by"), pair.get("right_by")}
        if login not in people:
            continue
        participated += 1
        if pair.get("consistent"):
            consistent += 1
    rate = (consistent / participated) if participated else None
    needed = int(policy["reviewer_qualification_consistent_entries"])
    return {
        "login": login,
        "consistent_entries": consistent,
        "participated": participated,
        "agreement_rate": rate,
        "qualified_reviewer": consistent >= needed,
        "note": "一致率不是准确率，也不用于排名或奖励",
    }


def parse_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise ValueError("缺少 YAML front matter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("front matter 未闭合")
    meta = yaml.safe_load(text[4:end]) or {}
    body = text[end + 5 :]
    return meta, body


def publication_pilot_logs(root: Path) -> list[Path]:
    """发布和统计用的研究日志。演练目录 pilot/_drill/ 不计入。"""
    logs = []
    pilot = root / "pilot"
    if not pilot.exists():
        return logs
    for path in sorted(pilot.rglob("*.md")):
        if path.name in {"_TEMPLATE.md", "README.md"}:
            continue
        if "_drill" in path.parts:
            continue
        logs.append(path)
    return logs


def pilot_errors(path: Path, text: str | None = None, policy: dict | None = None) -> list[str]:
    errors = []
    raw = text if text is not None else path.read_text(encoding="utf-8")
    label = str(path)
    try:
        meta, body = parse_front_matter(raw)
    except ValueError as exc:
        return [f"{label}: {exc}"]
    policy = policy or load_policy()
    required = (
        "glyph_id",
        "tier",
        "origin_source",
        "corpus_scope",
        "started",
        "last_updated",
        "researcher",
        "conclusion_level",
        "public",
        "second_reviewer",
        "missed_attestation_in_batch",
        "changelog",
    )
    for key in required:
        if key not in meta:
            errors.append(f"{label}: 缺少字段 {key}")
    level = meta.get("conclusion_level")
    if level not in PILOT_LEVEL_RANK:
        errors.append(f"{label}: conclusion_level 不在五档之内")
    if level in FORBIDDEN_STATUS_WORDS or level == "已破译":
        errors.append(f"{label}: 不得使用已破译")
    scope = str(meta.get("corpus_scope") or "").strip()
    if not scope and level in PILOT_LEVEL_RANK:
        if PILOT_LEVEL_RANK[level] > PILOT_LEVEL_RANK[PILOT_SCOPE_CEILING]:
            errors.append(f"{label}: corpus_scope 为空时结论最高只能到线索待查")
    if scope and (
        "检索日期" not in scope
        or "缀合库查询日期" not in scope
        or not re.search(r"\d{4}-\d{2}-\d{2}", scope)
    ):
        errors.append(
            f"{label}: corpus_scope 须记录著录书简称、ISO 检索日期，以及缀合库查询日期"
        )
    glyph_id = str(meta.get("glyph_id") or "").strip()
    in_drill = "_drill" in path.parts
    if in_drill:
        if not is_reserved_test_id(glyph_id, policy):
            errors.append(
                f"{label}: 演练记录只能使用测试编号段，且该段永不发给真实字形"
            )
    elif glyph_id and is_reserved_test_id(glyph_id, policy):
        errors.append(f"{label}: 测试编号段永不发给真实字形")
    if path.name != "_TEMPLATE.md" and not glyph_id:
        errors.append(f"{label}: glyph_id 必填")
    if meta.get("missed_attestation_in_batch") is True and level != "线索待查":
        errors.append(f"{label}: 发现漏掉辞例后必须降为线索待查")
    if meta.get("public") is True and level in HYPOTHESIS_LEVELS:
        reviewer = str(meta.get("second_reviewer") or "").strip()
        researcher = str(meta.get("researcher") or "").strip()
        if not reviewer or reviewer == researcher:
            errors.append(f"{label}: 候选假说公开前须另一名研究者复核")
    started = str(meta.get("started") or "")
    updated = str(meta.get("last_updated") or "")
    changelog = meta.get("changelog")
    if not isinstance(changelog, list):
        errors.append(f"{label}: changelog 必须是列表")
        changelog = []
    if started and updated and started != updated and not changelog:
        errors.append(f"{label}: 更新后必须写一行变更说明，降档也要保留旧记录")
    for heading in PILOT_HEADINGS:
        if heading not in body:
            errors.append(f"{label}: 缺少章节 {heading}")
    return errors


def strip_fenced_code(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def markdown_link_errors(root: Path) -> list[str]:
    errors = []
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in sorted(root.rglob("*.md")):
        if any(part in {".git", "data/downloads", "tools/logs"} for part in path.parts):
            continue
        if "site-packages" in path.parts:
            continue
        text = strip_fenced_code(path.read_text(encoding="utf-8"))
        for target in link_re.findall(text):
            target = target.strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            if target.startswith("#"):
                continue
            path_part, _, _anchor = target.partition("#")
            if not path_part:
                continue
            resolved = (path.parent / path_part).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{path.relative_to(root)}: 链接越出仓库 {target}")
                continue
            if not resolved.exists():
                errors.append(f"{path.relative_to(root)}: 链接不存在 {target}")
    return errors


def issue_form_errors(root: Path) -> list[str]:
    errors = []
    for relative, required_ids in ISSUE_FORMS.items():
        path = root / relative
        if not path.exists():
            errors.append(f"缺少 Issue 模板 {relative}")
            continue
        form = yaml.safe_load(path.read_text(encoding="utf-8"))
        found = set()
        for block in form.get("body") or []:
            block_id = block.get("id")
            validations = block.get("validations") or {}
            if block_id and validations.get("required") is True:
                found.add(block_id)
            if block.get("type") == "checkboxes":
                for option in (block.get("attributes") or {}).get("options") or []:
                    if option.get("required") is True and block_id:
                        found.add(block_id)
        missing = [item for item in required_ids if item not in found]
        if missing:
            errors.append(f"{relative}: 必填项缺失 {', '.join(missing)}")
    template = root / "docs" / "templates" / "counterexample.md"
    if not template.exists():
        errors.append("缺少反例评论模板 docs/templates/counterexample.md")
    else:
        text = template.read_text(encoding="utf-8")
        for heading in ("著录号与辞例原文", "与提案哪条论证冲突", "为何冲突", "可核查出处"):
            if heading not in text:
                errors.append(f"反例模板缺少栏目: {heading}")
    return errors


def image_file_errors(root: Path) -> list[str]:
    errors = []
    registry = root / "registry"
    suffixes = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".tif", ".tiff", ".bmp"}
    for path in registry.rglob("*"):
        if path.suffix.lower() in suffixes:
            errors.append(f"登记目录不得包含图像文件: {path.relative_to(root)}")
    return errors


def validate_repository(root: Path | None = None, now: datetime | None = None) -> list[str]:
    root = root or ROOT
    now = now or datetime.now(timezone.utc)
    policy = load_policy(root)
    errors: list[str] = []
    allowlist = load_domain_allowlist(root)
    try:
        table = load_normalize_table(root)
    except ValueError as exc:
        return [str(exc)]

    glyph_validator = schema_validator(root, "registry/schema/glyph.schema.json")
    group_validator = schema_validator(root, "registry/schema/group.schema.json")
    record_validator = schema_validator(root, "registry/schema/record.schema.json")
    cross_validator = schema_validator(root, "registry/schema/crosswalk.schema.json")
    entry_validator = schema_validator(root, "registry/schema/transcription.schema.json")
    ledger_validator = schema_validator(root, "registry/schema/id-ledger.schema.json")

    def collect(directory: str) -> dict[str, tuple[Path, dict]]:
        found = {}
        for path, doc in iter_yaml(root / directory):
            if not isinstance(doc, dict):
                errors.append(f"{path.relative_to(root)}: 必须是映射")
                continue
            glyph_id = doc.get("glyph_id")
            found[str(glyph_id)] = (path, doc)
        return found

    glyphs = collect("registry/glyphs")
    groups = collect("registry/groups")
    records = collect("registry/records")
    crosswalks = collect("registry/crosswalk")

    for glyph_id, (path, doc) in glyphs.items():
        label = str(path.relative_to(root))
        errors.extend(schema_errors(glyph_validator, doc, label))
        errors.extend(pointer_errors(doc, allowlist, label))
        if is_reserved_test_id(glyph_id, policy):
            errors.append(f"{label}: 测试编号段永不发给真实字形")
        if doc.get("example") and "示例数据，非真实释读" not in str(doc.get("example_notice")):
            errors.append(f"{label}: 示例必须标明“示例数据，非真实释读”")
        citation = str(doc.get("source_citation") or "")
        if not citation.strip() or not citation_ok(citation, policy):
            errors.append(f"{label}: source_citation 必须说明字编或论著将其列为存疑/未识")
        if doc.get("variant_relation") in {"已并合", "同字终判"}:
            errors.append(f"{label}: 新手任务不能写入字形归并终判")
        for related in doc.get("related_glyph_ids") or []:
            if related not in glyphs:
                errors.append(f"{label}: 关联编号不存在 {related}")

    for glyph_id, (path, doc) in groups.items():
        label = str(path.relative_to(root))
        errors.extend(schema_errors(group_validator, doc, label))
        errors.extend(pointer_errors(doc, allowlist, label))

    entries: list[tuple[Path, dict]] = []
    for path, doc in iter_yaml(root / "registry" / "transcriptions") + iter_yaml(
        root / "registry" / "dual-entries"
    ):
        label = str(path.relative_to(root))
        if not isinstance(doc, dict):
            errors.append(f"{label}: 必须是映射")
            continue
        errors.extend(schema_errors(entry_validator, doc, label))
        errors.extend(transcription_errors(doc, table, policy, label))
        errors.extend(pointer_errors(doc, allowlist, label))
        citation = str(doc.get("source_citation") or "")
        if not citation_ok(citation, policy):
            errors.append(f"{label}: source_citation 必须说明列为存疑/未识")
        if doc.get("glyph_id") not in glyphs:
            errors.append(f"{label}: glyph_id 尚未领号")
        entries.append((path, doc))

    record_ids = [doc.get("record_id") for _, doc in entries]
    if len(record_ids) != len(set(record_ids)):
        errors.append("辞例 record_id 重复")

    for glyph_id, (path, doc) in records.items():
        label = str(path.relative_to(root))
        errors.extend(schema_errors(record_validator, doc, label))
        errors.extend(pointer_errors(doc, allowlist, label))
        if doc.get("example") and "示例数据，非真实释读" not in str(doc.get("example_notice")):
            errors.append(f"{label}: 示例必须标明“示例数据，非真实释读”")
        errors.extend(review_errors(doc, policy, now))
        related_entries = [item for _, item in entries if item.get("glyph_id") == glyph_id]
        errors.extend(status_ceiling_blocks_endorsement(doc, related_entries, policy))

    for glyph_id, (path, doc) in crosswalks.items():
        label = str(path.relative_to(root))
        errors.extend(schema_errors(cross_validator, doc, label))
        errors.extend(pointer_errors(doc, allowlist, label))

    id_sets = [set(glyphs), set(groups), set(records), set(crosswalks)]
    if not all(item == id_sets[0] for item in id_sets):
        errors.append(
            "字形、组类、档案、crosswalk 的编号集合不一致: "
            + ", ".join(sorted(set().union(*id_sets)))
        )

    ledger_path = root / "registry" / "id-ledger.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    errors.extend(schema_errors(ledger_validator, ledger, "registry/id-ledger.json"))
    errors.extend(ledger_errors(ledger, policy, now))
    used_ids = {
        row["glyph_id"] for row in ledger.get("allocations", []) if row.get("state") == "used"
    }
    if used_ids != set(glyphs):
        errors.append("已使用编号必须且只能对应一份字头登记")
    for row in ledger.get("allocations", []):
        if row.get("state") == "abandoned" and row["glyph_id"] in glyphs:
            errors.append(f"废弃编号不得再有登记: {row['glyph_id']}")

    dual_root = root / "registry" / "dual-entries"
    if dual_root.exists():
        for folder in sorted(path for path in dual_root.iterdir() if path.is_dir()):
            files = sorted(folder.glob("*.yaml"))
            if len(files) == 1:
                continue
            if len(files) != 2:
                errors.append(f"{folder.relative_to(root)}: 双人录入在第三名复核前只能有两份")
                continue
            left = read_yaml(files[0])
            right = read_yaml(files[1])
            report = dual_report(left, right, table)
            if report["same_person"]:
                errors.append(f"{folder.relative_to(root)}: 两份录入人相同，不是独立双录")
            if report["conflicts"]:
                errors.append(f"{folder.relative_to(root)}: 双录不一致，禁止自动合并")

    errors.extend(image_file_errors(root))
    template = root / "pilot" / "_TEMPLATE.md"
    if not template.exists():
        errors.append("缺少 pilot/_TEMPLATE.md")
    else:
        template_text = template.read_text(encoding="utf-8")
        if "一形多用" not in template_text:
            errors.append("试点模板须提醒：甲骨文存在一形多用，只比字形不够")
        if "缀合库查询日期" not in template_text:
            errors.append("试点模板须说明 corpus_scope 记录缀合库查询日期")
    for path in sorted((root / "pilot").rglob("*.md")):
        if path.name == "README.md":
            continue
        errors.extend(pilot_errors(path, policy=policy))
    errors.extend(issue_form_errors(root))
    errors.extend(markdown_link_errors(root))

    candidate_path = root / "tools" / "examples" / "obsd-placeholder.json"
    if candidate_path.exists():
        from tools.interface import validate_model_output

        candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
        errors.extend(
            f"tools/examples/obsd-placeholder.json: {item}"
            for item in validate_model_output(candidate, root=root)
        )
    return errors


def counterevidence_window(start: datetime, days: int = 14) -> tuple[str, str]:
    start = start.astimezone(timezone.utc)
    end = start + timedelta(days=days)
    form = "%Y-%m-%dT%H:%M:%SZ"
    return start.strftime(form), end.strftime(form)
