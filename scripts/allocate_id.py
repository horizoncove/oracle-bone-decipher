#!/usr/bin/env python3
"""发出下一个不透明编号。测试段 OBD-900001–OBD-900099 会跳过，且永不复用。"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.obd.engine import allocate_id, load_policy


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="领号。默认只预览，不写文件。")
    parser.add_argument("--account", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--source-note", required=True)
    parser.add_argument("--write", action="store_true", help="写回 registry/id-ledger.json")
    parser.add_argument("--ledger", type=Path, default=ROOT / "registry" / "id-ledger.json")
    args = parser.parse_args(argv)
    policy = load_policy(ROOT)
    ledger = json.loads(args.ledger.read_text(encoding="utf-8"))
    row = allocate_id(
        ledger,
        args.account,
        args.description,
        args.source_note,
        datetime.now(timezone.utc),
        policy,
    )
    print(json.dumps(row, ensure_ascii=False, indent=2))
    if args.write:
        args.ledger.write_text(
            json.dumps(ledger, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"已写入 {args.ledger}", file=sys.stderr)
    else:
        print("未写入。确认去重后加 --write。编号一旦发出不改不复用。", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
