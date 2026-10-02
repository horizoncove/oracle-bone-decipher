# 治理

## 公益宣言

本项目是无偿服务国家的公益、非商业协作。项目不收费，不接受商业化运作，维护者不从项目获利。向中国文字博物馆提交论证报告同样是公益行为，不作为收费服务。

代码采用 MIT，社区释读内容采用 CC BY 4.0。这两种许可按其文本允许他人在遵守条款的前提下商业性再利用。公益宣言约束的是本项目怎么运营，不改写许可文本。详见 [LICENSE](LICENSE) 与 [LICENSE-CONTENT](LICENSE-CONTENT)。

## 角色

- 贡献者：领号、录入、查重、文献梳理、提交提案。
- 评审员：按固定清单对照著录号锁定辞例数和残缺程度，或裁定双录冲突。锁定必须由提案人以外的人完成。
- 满足条件的评审者：专家门是开放的。具体认定机制后续再定。在机制写明之前，不编制专家名单，不把任何提案标成“专家认可”。

不设需要个人口头拍板的环节。规则在 `registry/policy.json` 和本文件里。要改规则，就改这些公开文件。

## 投票

社区票只决定排队优先级，一人一票。有已合并贡献的 GitHub 账号可以投票，新号只能评论。票不能把“有争议”改成“认可”，也不能改变 `review_status`。

自动判定谁有投票资格，这一版没有做，见 [路线图](docs/ROADMAP.md)。书面规则只能挡住低成本刷票，挡不住有组织的重复账号。

## 状态上限

专家不足 2 人时，提案不得高于“可接受的候选”。当前认定机制未定，因此按不足 2 人处理，“专家认可”暂空置。

辞例数小于等于 2，或锁定后的残缺程度为重残，也不能高于“可接受的候选”。提案人自填的辞例数和残缺程度不生效。

“可接受的候选”必须带固定声明：未经专家评审，仅表示证据齐备、尚无已知反例。

数字阈值是经验设定，待校准，列在路线图阶段 0。

## 编号

`OBD-` 加六位。发出后不改不复用。`OBD-900001` 至 `OBD-900099` 永不发给真实字形。超过 30 天未使用的挂起编号标为废弃，编号仍然占用。每账号同时挂起不超过 5 个。5 与 30 是经验设定，待校准。

## English

The project does not charge and maintainers do not profit from it. MIT and CC BY 4.0 still allow reuse under those licenses. Expert endorsement is vacant until a public rule defines who may hold that role. Votes rank the queue only. Reserved ids OBD-900001–OBD-900099 are never issued for real graphs.
