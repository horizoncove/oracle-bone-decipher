# 链接探活记录

每周工作流 `.github/workflows/link-probe.yml` 运行 `python scripts/check_links.py --probe`。脚本把当次结果追加到 [link-probe-log.jsonl](link-probe-log.jsonl)，一行一条，只追加，不改旧行。

探活只访问登记记录里已经出现、且主机名在 [允许表](../registry/allowed-link-domains.txt) 里的链接。失败写在该行的 `failures` 中，不处罚，也不修改登记状态、`conclusion_level` 或 `status_tier`。没有 `--probe` 时只核对域名，不写记录。域名未登记时脚本直接停下，不探活，也不追加记录。

字段示例（不是一次真实探活）：

```json
{"checked_at": "2026-10-04T06:00:00Z", "failure_count": 0, "failures": [], "note": "探活失败只记录，不处罚，也不改登记状态", "url_count": 0, "urls": []}
```

## English

The weekly workflow runs `python scripts/check_links.py --probe` and appends one JSON line to `link-probe-log.jsonl`. Probes use only URLs already present in registry records whose hostnames are already allowlisted. A failure is a line in that log. It does not penalize anyone and does not change registry status or conclusion level. The fenced JSON above shows the fields; it is not a real probe.
