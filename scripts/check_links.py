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


def text_urls(text: str) -> list[str]:
    """从原文抽出 URL。JSON/YAML 的结束引号和逗号不属于链接。"""
    found = []
    for match in URL_RE.findall(text):
        # 原文扫描会把 JSON 收尾的引号、逗号、右花括号吃进匹配。
        cleaned = match.rstrip("\"',}")
        if cleaned:
            found.append(cleaned)
    return found


def registry_urls(root: Path) -> list[str]:
    """登记记录中的外链。

    ``registry/schema/`` 里的 ``$schema`` 是 JSON Schema 规范标识
    （https://json-schema.org/draft/2020-12/schema），``$id`` 是模式自身的标识。
    它们不是著录或图像指针，不参加域名允许表检查。
    """
    found = []
    registry = root / "registry"
    schema_dir = registry / "schema"
    for pattern in ("*.yaml", "*.json"):
        for path in sorted(registry.rglob(pattern)):
            if schema_dir in path.parents:
                continue
            found.extend(text_urls(path.read_text(encoding="utf-8")))
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
