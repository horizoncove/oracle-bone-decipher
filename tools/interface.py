"""统一的候选生成接口。

模型只能给出 machine-suggestion。分类器在已知类里选择，对真正未释字没有依据。
AI 相似度不算证据。调用会把输入和输出记到日志。
"""

from __future__ import annotations

import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = Path(__file__).resolve().parent / "schema" / "candidate.schema.json"
SCORE_SEMANTICS = "模型相似度，不是概率，更不是正确性"
MACHINE_STATUS = "machine-suggestion"
IMAGE_REF_RE = re.compile(r"(?i)(?:^|.*)\.(?:png|jpe?g|gif|webp|svg|tiff?|bmp)$|data:image/")


def _validator() -> Draft202012Validator:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def validate_candidate_document(document: dict) -> list[str]:
    errors = []
    for error in sorted(_validator().iter_errors(document), key=lambda item: list(item.path)):
        path = "/".join(str(part) for part in error.path) or "(root)"
        errors.append(f"{path}: {error.message}")
    if document.get("status") != MACHINE_STATUS:
        errors.append("status 必须为 machine-suggestion")
    if document.get("score_semantics") != SCORE_SEMANTICS:
        errors.append("score_semantics 被改写")
    if document.get("closed_set") is not True:
        errors.append("closed_set 必须为 true：分类器只能在已知类里选择")
    input_ref = str(document.get("input_ref") or "")
    if IMAGE_REF_RE.search(input_ref):
        errors.append("input_ref 只能是指针，不能是图像")
    return errors


def validate_model_output(document: dict, root: Path | None = None) -> list[str]:
    del root
    errors = validate_candidate_document(document)
    if document.get("human_review") is not None:
        errors.append("模型输出的 human_review 必须为 null，只能由人事后填写")
    return errors


def assert_not_used_as_evidence(record: dict) -> list[str]:
    blob = json.dumps(record.get("evidence", []), ensure_ascii=False)
    errors = []
    if "machine-suggestion" in blob or "cand-" in blob or "candidate_id" in blob:
        errors.append("提案或档案的证据字段不得引用机器候选")
    return errors


def append_call_log(input_payload: dict, output_payload: dict, log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    row = {"input": input_payload, "output": output_payload}
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def build_machine_suggestion(
    *,
    target_glyph_id: str,
    input_ref: str,
    model: dict,
    training_data: dict,
    log_path: Path,
    suggested_reading: str | None = None,
    rank: int | None = None,
    score: float | None = None,
) -> dict:
    if IMAGE_REF_RE.search(input_ref):
        raise ValueError("input_ref 只能是指针，不能是图像")
    document = {
        "candidate_id": "cand-" + uuid.uuid4().hex[:12],
        "target_glyph_id": target_glyph_id,
        "suggested_reading": suggested_reading,
        "rank": rank,
        "score": score,
        "score_semantics": SCORE_SEMANTICS,
        "model": model,
        "training_data": training_data,
        "input_ref": input_ref,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "run_id": uuid.uuid4().hex,
        "status": MACHINE_STATUS,
        "closed_set": True,
        "human_review": None,
    }
    errors = validate_model_output(document)
    if errors:
        raise ValueError("; ".join(errors))
    append_call_log(
        {
            "target_glyph_id": target_glyph_id,
            "input_ref": input_ref,
            "model": model.get("name"),
        },
        document,
        log_path,
    )
    return document
