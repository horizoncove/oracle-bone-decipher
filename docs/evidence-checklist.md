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

直接不能成立的论证：

- 只凭字形相似，或只凭 AI 相似度
- 单一辞例的灵感式释读
- 没有著录号
- 改动字形来迎合释读
- 不可证伪
- 用上古文明想象或玄学代替证据

AI 输出的 `status` 固定为 `machine-suggestion`。提案的 `evidence` 字段引用它会校验失败。

## English

The checklist is procedural. A model similarity score is not evidence. One graph can have more than one use, so usage comes before shape.
