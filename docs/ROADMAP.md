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

公开来源摸底（检索日 2026-10-02）见 [来源调查](source-survey-2026-10-02.md)。《综理表》与《待问编》的合法免费全文这次没有在公开网页找到。另一次摸底见 [可读来源调查](source-survey-2026-10-02-readable.md)。书目指针在 `pilot/_drill/OBD-900002.md`：保留测试号，不进发布，也不发给真实字形。

本阶段要做、现在还没做：

- 缀合库检索日期晚于 `corpus_scope` 里的日期时，自动加“范围过期，需复查”标签。只提醒，不自动降档。是否降档，由复核者看过新增辞例后再决定。
- 把每周链接探活的结果整理成可追踪的记录。探活脚本已经有了，失败不处罚。

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

Stages 0–3. Every numeric threshold above is empirical and not yet calibrated. The reserved drill ids are not a threshold. Stage 1 links two 2026-10-02 public-web surveys. They are investigation records, not decipherments. A bibliographic pointer sits in `pilot/_drill/` under a reserved test id and is excluded from publication. Stale rejoining-corpus searches will later get a reminder label only; nothing is downgraded automatically. Duplicate-proposal search, automatic vote eligibility, collusion sampling, and translation sync are listed here and are not built.
