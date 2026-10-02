#!/usr/bin/env python3
"""运行登记、辞例、试点日志、模板与 Markdown 链接校验。"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.obd.engine import validate_repository


def main() -> int:
    errors = validate_repository(ROOT)
    if errors:
        print("\n".join(errors))
        print(f"失败：{len(errors)} 项")
        return 1
    print("校验通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
