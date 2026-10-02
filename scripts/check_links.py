#!/usr/bin/env python3
"""检查登记记录中的外链域名。--probe 才访问网络，失败只打印，不改状态。"""

from __future__ import annotations

import argparse
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.obd.engine import URL_RE, load_domain_allowlist


def registry_urls(root: Path) -> list[str]:
    found = []
    registry = root / "registry"
    for path in sorted(registry.rglob("*.yaml")):
        text = path.read_text(encoding="utf-8")
        found.extend(URL_RE.findall(text))
    for path in sorted(registry.rglob("*.json")):
        text = path.read_text(encoding="utf-8")
        found.extend(URL_RE.findall(text))
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    args = parser.parse_args(argv)
    allowlist = load_domain_allowlist(ROOT)
    urls = registry_urls(ROOT)
    bad = []
    from urllib.parse import urlparse

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
    failures = []
    for url in urls:
        request = urllib.request.Request(url, method="HEAD")
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                if response.status >= 400:
                    failures.append(f"{url} -> {response.status}")
        except Exception as exc:  # noqa: BLE001 — 探活失败只汇报
            failures.append(f"{url} -> {exc}")
    if failures:
        print("链接探活未成功（只提醒，不自动处罚）:")
        print("\n".join(failures))
        return 1
    print("探活完成")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
