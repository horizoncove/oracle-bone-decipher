"""OBSD 适配器占位。

不调用上游演示站，不加载权重，不编造释读或分数。
公开仓库 https://github.com/guanhaisu/OBSD 已于 2026-10-02 核对，见 tools/README.md。
本文件不下载权重或数据集。查不到的字段写 unknown 或在说明里标待确认。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.interface import IMAGE_REF_RE, build_machine_suggestion

DEFAULT_LOG = ROOT / "tools" / "logs" / "calls.jsonl"


def generate(glyph_id: str, input_ref: str | None = None, log_path: Path = DEFAULT_LOG) -> dict:
    pointer = input_ref or f"glyph:{glyph_id}"
    if IMAGE_REF_RE.search(pointer):
        raise ValueError("OBSD 适配器只接受指针。图像不进入本仓库，也不传给占位接口。")
    return build_machine_suggestion(
        target_glyph_id=glyph_id,
        input_ref=pointer,
        suggested_reading=None,
        rank=None,
        score=None,
        model={
            "name": "OBSD",
            "version": "unknown",
            "weights_source": "https://github.com/guanhaisu/OBSD",
        },
        training_data={
            "name": "上游 README 与论文提到的训练数据；本适配器未绑定具体快照",
            "license": "unknown",
        },
        log_path=log_path,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="OBSD 占位适配器，不执行推理")
    parser.add_argument("--glyph-id", required=True)
    parser.add_argument("--input-ref", default=None)
    parser.add_argument("--image", default=None, help="若提供则直接拒绝")
    args = parser.parse_args(argv)
    if args.image:
        print("拒绝：输入只能是指针，不能是图像文件。", file=sys.stderr)
        return 2
    document = generate(args.glyph_id, args.input_ref)
    print(json.dumps(document, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
