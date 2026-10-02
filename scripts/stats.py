#!/usr/bin/env python3
"""发布与统计口径。pilot/_drill/ 不计入。测试编号段不计入真实字形。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.obd.engine import is_reserved_test_id, load_policy, publication_pilot_logs


def main() -> int:
    policy = load_policy(ROOT)
    published = publication_pilot_logs(ROOT)
    drill = [
        path
        for path in sorted((ROOT / "pilot").rglob("*.md"))
        if "_drill" in path.parts and path.name != "README.md"
    ]
    glyphs = sorted((ROOT / "registry" / "glyphs").glob("*.yaml"))
    real_glyphs = []
    for path in glyphs:
        glyph_id = path.stem
        if is_reserved_test_id(glyph_id, policy):
            print(f"错误：真实登记使用了测试编号 {glyph_id}", file=sys.stderr)
            return 1
        real_glyphs.append(glyph_id)
    summary = {
        "real_glyph_ids": real_glyphs,
        "published_pilot_logs": [str(path.relative_to(ROOT)) for path in published],
        "excluded_drill_logs": [str(path.relative_to(ROOT)) for path in drill],
        "reserved_test_ids": "OBD-900001–OBD-900099",
        "note": "演练目录参与校验，但发布和统计排除它。测试编号永不发给真实字形。",
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
