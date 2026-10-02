# 候选接口

AI 相似度不算证据。

统一记录的字段见 `schema/candidate.schema.json`：

- `candidate_id`
- `target_glyph_id`
- `suggested_reading`（可空）
- `rank` 与 `score`
- `score_semantics` 固定为“模型相似度，不是概率，更不是正确性”
- `model`：名称、版本、权重来源
- `training_data`：名称和许可；许可不明写 `unknown`
- `input_ref`：只存指针，不存图像
- `generated_at` 与 `run_id`
- `status` 固定 `machine-suggestion`
- `closed_set` 固定 `true`。分类器只能在已知类里选，对真正未释字没有依据
- `human_review` 在模型输出里必须是 `null`，只能由人事后填写

`status` 不是这个固定值，校验失败。登记档案的 `evidence` 不能引用这些记录。每次调用把输入和输出追加到 `tools/logs/`，该目录不入库。

## OBSD 适配器

占位实现：`python -m tools.adapters.obsd --glyph-id OBD-000001`

它不下载权重，不访问演示站，不填写释读，也不编造分数。`version` 与训练数据许可都是 `unknown`。

已核对的上游情况：

- 代码仓库：<https://github.com/guanhaisu/OBSD>。2026-10-02 复核：该 URL 是公开仓库，GitHub 描述为 “Deciphering Oracle Bone Language with Diffusion Models (ACL 2024 Best Paper)”；API 的 `license` 字段为空，根目录没有 LICENSE 文件。代码许可仍待确认。本仓库不收录权重或数据集。
- 论文：<https://arxiv.org/abs/2406.00684>，Anthology 页：<https://aclanthology.org/2024.acl-long.831/>。同一天打开的摘要页上，arXiv 许可图标指向 CC BY-NC-ND 4.0；Anthology 写明 2016 年及以后的材料为 CC BY 4.0。两处文本不一致，本仓库不裁定，只外链，不保存 PDF。
- 上游 README 里的演示地址是 <http://vlrlabmonkey.xyz:8225/>。本仓库不调用它，也不监测它是否在线。
- 推理入口是 `OBS_Diffusion/eval_diffusion.py`，默认配置文件名是 `configs.yml`。README 正文写成 `configs.yaml`，与仓库中的文件名不一致。
- 该脚本在分布式环境下把生成图像写到配置里的目录，没有一个返回校准置信度的稳定函数接口。因此这里不能填写 score。置信度接口待确认。
- 训练数据的具体快照和许可待确认。论文讨论了 HUST-OBC 等数据；那些数据的许可见 [docs/datasets.md](../docs/datasets.md)，不能因为本适配器存在就被再许可。

## English

Model output is a machine suggestion. The OBSD adapter is a stub. It does not invent a reading or a score. On 2026-10-02 the public repository URL was rechecked; the repository still has no LICENSE file. The arXiv abstract page and the ACL Anthology page do not state the same license. Weights and datasets are not vendored. Several upstream interface details remain unconfirmed.
