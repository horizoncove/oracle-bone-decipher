# 释文符号

这些符号是本项目自定义的，不是学界统一标准。是否对齐某部著录的体例，待确认。

| 符号 | 含义 |
| --- | --- |
| □ | 缺一字 |
| … | 缺字数不明 |
| 【】 | 推补之字 |
| { } | 合文 |
| 々 | 重文。原字写在 `note` |
| 字后 ? | 摹写或辨认存疑 |

释文用繁体、严式隶定，单行。不得擅自通假改字；通假只写在 `note`。没有 Unicode 的字形写成 `〔OBD-######〕`，不要把 IDS 写进释文。IDS 只作字头登记里的 `ids_description`。没有编号的字形必须先领号。

录入前先用 `data/normalize.csv` 做兼容汉字替换，再做 NFC。这张表目前只有表头，待古文字研究员审定，不能当成已经核定的映射。

校验里的数量关系是经验设定，待校准：

- `complete` 不能出现 □、… 或推补
- 出现推补则不能是 `complete`
- `minor` 的 □ 不超过 2 个，且不能有 …
- `severe` 必须有 □ 或 …

括号必须成对。归一化后两份双录完全相同才算一致，否则按 `catalog_ref`、`damage_level` 和符号差异逐项列出。冲突不自动合并。两人同错而一致时脚本查不出，要抽查原书。

## English

The signs are local conventions. Whether they match a published editorial standard is unconfirmed. The compatibility-character table is an empty placeholder.
