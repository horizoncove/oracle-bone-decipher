# 如何参与

先读 [新手第一任务](docs/first-tasks.md) 和 [行为准则](CODE_OF_CONDUCT.md)。

## 开放任务

- 辞例录入与核对。模板字段见 `registry/schema/transcription.schema.json`，符号见 [释文约定](docs/transcription-conventions.md)。
- 文献梳理。只归纳，附原书页码，不下判断。
- 异体整理。只能标“疑似同字”。
- 检索与查重。判断某个说法是不是早已有人提出，并写下可核查出处。

## 新手不要单独做

字形归并终判、残辞补缺与断句、分期分组判定、把状态写成已有定论。

## 领号

用 Issue 模板“申请字头编号”，写来源和文字描述，不要上传图像。两名复核者之一确认不是重复编号后，维护者运行：

```bash
python scripts/allocate_id.py --account LOGIN --description "..." --source-note "..." --write
```

默认不加 `--write` 只预览。测试段 OBD-900001 至 OBD-900099 会跳过。演练写到 `pilot/_drill/`，校验会跑，但 `python scripts/stats.py` 不把它算进发布。

## 双录

两人各交一份，提交时互不查看。然后：

```bash
python scripts/compare_entries.py
```

一致率不是准确率，不用于排名或奖励，只用于复核者资格（3 条后来核对一致的录入；3 是经验设定，待校准）。冲突不自动合并。

## 本地校验

```bash
pip install -r requirements-dev.txt
python scripts/validate_all.py
python -m unittest discover -s tests -v
```

拉取请求会跑同样的校验。不要提交 `data/downloads/` 里的数据集，也不要提交图像。

## 提案

用“释读提案”模板。证据清单见 [docs/evidence-checklist.md](docs/evidence-checklist.md)。不要把机器候选写进证据。

## English

Start with the first-task page. Do not upload images. Reserved drill ids are never issued for real graphs. Agreement rate is not accuracy and is not a ranking.
