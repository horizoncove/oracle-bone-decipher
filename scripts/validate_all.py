#!/usr/bin/env python3
"""运行登记、辞例、试点日志、模板与 Markdown 链接校验。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.obd.engine import (  # noqa: E402
    SCOPE_STALE_LABEL,
    repository_scope_reminders,
    validate_repository,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="运行登记、辞例、试点日志、模板与 Markdown 链接校验。")
    parser.add_argument(
        "--rejoin-search-date",
        default=None,
        help=(
            "缀合库检索日期（YYYY-MM-DD）。晚于某条日志 corpus_scope 里的缀合库查询日期时，"
            "打印提醒标签。不改写文件，也不因此改变退出码。"
        ),
    )
    args = parser.parse_args(argv)
    errors = validate_repository(ROOT)
    if errors:
        print("\n".join(errors))
        print(f"失败：{len(errors)} 项")
        code = 1
    else:
        print("校验通过")
        code = 0
    if args.rejoin_search_date:
        reminders = repository_scope_reminders(ROOT, args.rejoin_search_date)
        if not reminders:
            print("范围提醒：没有晚于 corpus_scope 缀合库查询日期的检索。")
        else:
            print("范围提醒（只提醒，不自动降档）:")
            for item in reminders:
                tier = item.get("status_tier")
                if tier is None:
                    tier = item.get("tier")
                print(
                    f"{item.get('path')}: {SCOPE_STALE_LABEL}"
                    f"；conclusion_level={item.get('conclusion_level')}"
                    f"；status_tier={tier}"
                )
    return code


if __name__ == "__main__":
    raise SystemExit(main())
