#!/usr/bin/env python3
"""列出外部数据集。只有 HUST-OBC 可以下载到 data/downloads/，且不入库。

OBC306 与 Oracle-50K 许可未明，本脚本拒绝下载。
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOWNLOAD_ROOT = ROOT / "data" / "downloads"

# 论文写明 CC BY-NC 4.0。Figshare API 元数据写成 CC BY 4.0，两处不一致，待确认。
# 下载地址来自 Figshare 公开 API（article 25040543，file 48465988），本仓库不转存文件。
HUST_OBC = {
    "name": "HUST-OBC",
    "paper": "https://doi.org/10.1038/s41597-024-03807-x",
    "figshare": "https://doi.org/10.6084/m9.figshare.25040543.v3",
    "download_url": "https://ndownloader.figshare.com/files/48465988",
    "md5": "7138be414ebc8c9262ecda38b7fd9e84",
    "code": "https://github.com/Pengjie-W/HUST-OBC",
    "modelscope": "https://www.modelscope.cn/datasets/wpj2003/HUST-OBC",
    "license": "论文标注 CC BY-NC 4.0；Figshare 元数据为 CC BY 4.0（待确认）",
    "commercial": False,
    "in_repo": False,
}

REFUSED = {
    "obc306": "许可未明，标为待确认，不使用，不下载。",
    "oracle-50k": "仓库未见 LICENSE，数据来自第三方站点，待确认，不使用，不下载。",
}


def decision(name: str) -> str:
    key = name.strip().lower()
    if key in {"hust-obc", "hust_obc"}:
        return "external-noncommercial"
    if key in REFUSED:
        return "refuse"
    return "unknown"


def download_hust_obc(dest: Path) -> int:
    dest.mkdir(parents=True, exist_ok=True)
    target = dest / "HUST-OBC.zip"
    try:
        dest.resolve().relative_to(DOWNLOAD_ROOT.resolve())
    except ValueError:
        print("只能下载到 data/downloads/ 之下。", file=sys.stderr)
        return 2
    print(f"下载 {HUST_OBC['download_url']}")
    urllib.request.urlretrieve(HUST_OBC["download_url"], target)
    digest = hashlib.md5(target.read_bytes()).hexdigest()
    if digest != HUST_OBC["md5"]:
        print(f"MD5 不符：{digest} != {HUST_OBC['md5']}", file=sys.stderr)
        return 1
    print(f"已保存 {target}。不要把该文件提交进 git。")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="外部数据集下载。默认只列出，不下载。")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--dataset", default="")
    parser.add_argument("--dest", type=Path, default=DOWNLOAD_ROOT / "hust-obc")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--acknowledge-paper-nc", action="store_true")
    args = parser.parse_args(argv)
    if args.list or not args.dataset:
        print(json_dumps_sources())
        return 0
    kind = decision(args.dataset)
    if kind == "refuse":
        print(REFUSED.get(args.dataset.lower(), "待确认，不使用"))
        return 2
    if kind != "external-noncommercial":
        print("未知数据集。待确认，不使用。")
        return 2
    print(HUST_OBC["license"])
    print("本仓库不收录该数据集。非商业限制以论文 CC BY-NC 4.0 为准，直至 Figshare 元数据差异被确认。")
    if not args.execute:
        print("未下载。若你接受论文的非商业条款，可加 --execute --acknowledge-paper-nc。")
        return 0
    if not args.acknowledge_paper_nc:
        print("拒绝下载：需要 --acknowledge-paper-nc。", file=sys.stderr)
        return 2
    return download_hust_obc(args.dest)


def json_dumps_sources() -> str:
    import json

    payload = {
        "hust-obc": HUST_OBC,
        "refused": REFUSED,
        "note": "著录书释文能否录入，版权状态待确认。详见 docs/datasets.md。",
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    raise SystemExit(main())
