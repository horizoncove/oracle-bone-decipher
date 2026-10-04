# 路线图

阶段里的天数、次数和条数都是经验设定，待校准。测试编号段 OBD-900001 至 OBD-900099 不是待校准的阈值，而是保留段，永不发给真实字形。

## 阶段 0

本仓库这一版：三层指针登记、Schema、校验工作流、双录比对、候选接口占位、试点日志模板、演练目录。

经验设定，待校准：

- 辞例数小于等于 2 则不能高于“可接受的候选”
- `minor` 的 □ 不超过 2
- 反证期 14 天，回应 7 天
- 每账号挂起未录入编号不超过 5，超过 30 天标废弃
- 复核者资格为 3 条核对一致的录入
- 同一提案未成形反例不超过 3 条
- 反例被判不成立累计 5 次，暂停 30 天
- 进入“可接受的候选”至少 2 名互不相关的复核者

## 阶段 1

用试点字的研究日志试跑阶段 0 的规则。演练继续放在 `pilot/_drill/`，不进发布和统计。

公开网页摸底记到 2026-10-04b。这些文件是调查记录，不是释读：

- [来源调查（2026-10-02）](source-survey-2026-10-02.md)
- [可读来源调查（2026-10-02）](source-survey-2026-10-02-readable.md)
- [来源调查（2026-10-04）](source-survey-2026-10-04.md)
- [来源调查（2026-10-04b）](source-survey-2026-10-04b.md)

《综理表》与《待问编》的合法公开全文，仍以 2026-10-02 的调查为准：没有找到。这里不重开。书目指针在 `pilot/_drill/`，用保留测试号，不进发布，也不发给真实字形。

本阶段两项工程：

- 缀合库检索日期晚于 `corpus_scope` 里记下的缀合库查询日期时，自动加上提醒标签“范围过期，需复查”（GitHub 标签名 `scope-stale-review`）。只提醒，不自动降档，不改 `conclusion_level` 或 `status_tier`。是否降档，由复核者看过新增辞例后再决定。`apply_scope_stale_reminder` 只返回带提醒的副本，不把标签写回日志。没有可比日期时不加标签。需要对照某次检索时，运行 `python scripts/validate_all.py --rejoin-search-date YYYY-MM-DD`，该参数不改变校验退出码。
- 每周链接探活仍由 `scripts/check_links.py --probe` 执行，并追加一行到 [链接探活记录](link-probe-log.md)（`docs/link-probe-log.jsonl`）。失败只写进这条记录，不处罚，也不改登记状态。探活只访问登记记录里已经出现、且主机名已在允许表中的链接。

## 阶段 2

在试点结果出来之后，再决定要不要放行 `status_tier` 的第三档，以及著录号统一到哪一套。后者仍待确认。`data/normalize.csv` 要等古文字研究员审定后才填行。专家档的认定机制仍是后续再定；未写明之前不启用“专家认可”。

## 阶段 3

证据包可以复现、版权已核实、专家档已按公开规则启用之后，才按报告模板准备提交。对象以中国文字博物馆为主。投递方式待补充。在此之前不发送。

## 只列在这里、这一版不实现

- 重复提案检索
- 投票资格自动判定
- 串通抽查。高度一致只供以后人工查看，不自动处罚
- 译文同步。日、韩、法、德目录只是占位，以中文版为准

## English

Stages 0–3. Every numeric threshold above is empirical and not yet calibrated. The reserved drill ids are not a threshold. Stage 1 links the public-web surveys through 2026-10-04b. They are investigation records, not decipherments. Bibliographic pointers sit in `pilot/_drill/` under reserved test ids and are excluded from publication. A rejoining-corpus search dated later than the rejoining-corpus date stored in `corpus_scope` adds the reminder label `scope-stale-review` (“范围过期，需复查”) on a returned copy only; `conclusion_level` and `status_tier` are not downgraded, and the log file is not rewritten. Weekly link probes append a line to `docs/link-probe-log.jsonl`. A failed probe is a record, not a penalty. Duplicate-proposal search, automatic vote eligibility, collusion sampling, and translation sync are listed here and are not built.
