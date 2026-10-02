#!/usr/bin/env python3
"""计算 14 天（UTC）反证期窗口。天数是经验设定，待校准。"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.obd.engine import counterevidence_window, load_policy


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--github-output", action="store_true")
    args = parser.parse_args(argv)
    policy = load_policy(ROOT)
    start, end = counterevidence_window(
        datetime.now(timezone.utc),
        days=int(policy["counterevidence_days"]),
    )
    if args.github_output:
        path = os.environ.get("GITHUB_OUTPUT")
        if not path:
            print("缺少 GITHUB_OUTPUT", file=sys.stderr)
            return 2
        with open(path, "a", encoding="utf-8") as handle:
            handle.write(f"start={start}\nend={end}\n")
    print(f"{start} {end}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
