#!/usr/bin/env python3
"""检查登记记录中的外链域名。--probe 才访问网络，失败只记录，不改状态。"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.obd.engine import URL_RE, load_domain_allowlist

DEFAULT_PROBE_LOG = Path("docs") / "link-probe-log.jsonl"
PROBE_NOTE = "探活失败只记录，不处罚，也不改登记状态"


def text_urls(text: str) -> list[str]:
    """从原文抽出 URL。JSON/YAML 的结束引号和逗号不属于链接。"""
    found = []
    for match in URL_RE.findall(text):
        # 原文扫描会把 JSON 收尾的引号、逗号、右花括号吃进匹配。
        cleaned = match.rstrip("\"',}")
        if cleaned:
            found.append(cleaned)
    return found


def registry_urls(root: Path) -> list[str]:
    """登记记录中的外链。

    ``registry/schema/`` 里的 ``$schema`` 是 JSON Schema 规范标识
    （https://json-schema.org/draft/2020-12/schema），``$id`` 是模式自身的标识。
    它们不是著录或图像指针，不参加域名允许表检查。
    """
    found = []
    registry = root / "registry"
    schema_dir = registry / "schema"
    for pattern in ("*.yaml", "*.json"):
        for path in sorted(registry.rglob(pattern)):
            if schema_dir in path.parents:
                continue
            found.extend(text_urls(path.read_text(encoding="utf-8")))
    return found


def probe_url(url: str, timeout: int = 20) -> str | None:
    """访问一条链接。失败时返回说明，成功返回 None。不改登记状态。"""
    request = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            if response.status >= 400:
                return f"{url} -> {response.status}"
    except Exception as exc:  # noqa: BLE001 — 探活失败只汇报
        return f"{url} -> {exc}"
    return None


def probe_registered_urls(urls: list[str], allowlist: set[str]) -> tuple[list[str], list[str]]:
    """只探活主机名已在允许表中的链接。返回 (已探活的 url, 失败说明)。"""
    probed = []
    failures = []
    for url in urls:
        host = (urlparse(url).hostname or "").lower()
        if host not in allowlist:
            continue
        probed.append(url)
        failure = probe_url(url)
        if failure:
            failures.append(failure)
    return probed, failures


def build_probe_record(
    urls: list[str],
    failures: list[str],
    checked_at: datetime | None = None,
) -> dict:
    """一条探活记录。不含结论档，失败也不表示处罚。"""
    checked_at = checked_at or datetime.now(timezone.utc)
    if checked_at.tzinfo is None:
        checked_at = checked_at.replace(tzinfo=timezone.utc)
    else:
        checked_at = checked_at.astimezone(timezone.utc)
    return {
        "checked_at": checked_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "url_count": len(urls),
        "urls": list(urls),
        "failure_count": len(failures),
        "failures": list(failures),
        "note": PROBE_NOTE,
    }


def append_probe_record(path: Path, record: dict) -> None:
    """追加一行 JSON。不改写已有行。文件末尾若没有换行，先补换行再写。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
    prefix = ""
    if path.exists() and path.stat().st_size:
        with path.open("rb") as handle:
            handle.seek(-1, 2)
            if handle.read(1) != b"\n":
                prefix = "\n"
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(prefix + payload)


def resolve_probe_log(root: Path, raw: str | None) -> Path:
    if not raw:
        return root / DEFAULT_PROBE_LOG
    path = Path(raw)
    if not path.is_absolute():
        path = root / path
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument(
        "--record",
        default=None,
        help="探活记录追加到这个 jsonl。--probe 时默认 docs/link-probe-log.jsonl",
    )
    args = parser.parse_args(argv)
    allowlist = load_domain_allowlist(ROOT)
    urls = registry_urls(ROOT)
    bad = []
    for url in urls:
        host = (urlparse(url).hostname or "").lower()
        if host not in allowlist:
            bad.append(url)
    if bad:
        print("未登记域名:")
        print("\n".join(bad))
        return 1
    print(f"登记记录中的 URL：{len(urls)}。域名均已登记，或没有 URL。")
    if not args.probe:
        return 0
    probed, failures = probe_registered_urls(urls, allowlist)
    record = build_probe_record(probed, failures)
    record_path = resolve_probe_log(ROOT, args.record)
    append_probe_record(record_path, record)
    print(f"探活记录已追加：{record_path}")
    if failures:
        print("链接探活未成功（只提醒，不自动处罚）:")
        print("\n".join(failures))
        return 1
    print("探活完成")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
