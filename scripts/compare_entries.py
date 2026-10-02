#!/usr/bin/env python3
"""比对双人独立录入。归一化后完全相同才算一致。冲突不自动合并。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.obd.engine import dual_report, load_normalize_table, read_yaml


def main() -> int:
    table = load_normalize_table(ROOT)
    root = ROOT / "registry" / "dual-entries"
    failed = False
    if not root.exists():
        print("没有双录目录")
        return 0
    for folder in sorted(path for path in root.iterdir() if path.is_dir()):
        files = sorted(folder.glob("*.yaml"))
        if len(files) < 2:
            print(f"{folder.name}: 等待第二份，暂不比对")
            continue
        if len(files) != 2:
            print(f"{folder.name}: 复核前只能有两份")
            failed = True
            continue
        report = dual_report(read_yaml(files[0]), read_yaml(files[1]), table)
        print(json.dumps({"pair": folder.name, **report}, ensure_ascii=False))
        if not report["consistent"]:
            failed = True
    if failed:
        print("存在冲突。不要自动合并，交给没看过前两份的第三名复核者对照原书裁定。")
        print("两人同错而一致时，本脚本查不出来，需要抽查回原书。")
        return 1
    print("已提交的双录一致。一致率不是准确率。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
