# 提案证据清单

中文为主。English summary at the end.

形式门只检查这些项目是否齐，不代替释读判断。

1. 著录号及版本。
2. 分期、组类与出处。分期分组的终判不是新手任务；未知就写 `unknown`。
3. 全部可见辞例，不得挑选。
4. 释读后逐条通读。
5. 字形演变链和内部证据：异体、对贞、同辞互换。甲骨文有一形多用，只比字形不够，要先看用法。
6. 与已有释读比较。
7. 声韵、训诂只作辅助。

`source_citation` 必填，而且必须能看出某部字编或论著把该形列为存疑或未识。缺失则校验失败。

每条证据的出处栏有“是否需登录”，只能填“是”或“否”。选“是”的条目只能作个人线索：别人无法免登录复核，这和“证据必须可核查”冲突。研究日志里只要含一条这样的证据，`conclusion_level` 最高到“线索待查”。校验脚本会检查。缺页码的条目仍然不算证据。

直接不能成立的论证：

- 只凭字形相似，或只凭 AI 相似度
- 单一辞例的灵感式释读
- 没有著录号
- 改动字形来迎合释读
- 不可证伪
- 用上古文明想象或玄学代替证据

AI 输出的 `status` 固定为 `machine-suggestion`。提案的 `evidence` 字段引用它会校验失败。

## English

The checklist is procedural. A model similarity score is not evidence. One graph can have more than one use, so usage comes before shape. A source that requires login is only a personal clue. A research log that includes one cannot go beyond “clue to be checked.”
