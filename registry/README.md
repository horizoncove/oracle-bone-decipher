# 登记

三层分开存放，用同一个不透明编号连起来。编号形状是 `OBD-` 加六位数字，发出后不改、不复用。

| 层 | 目录 | 内容 |
| --- | --- | --- |
| 字形 | `glyphs/` | 来源、片号、摹写状态、疑似同字或待并合。图像只写“待查原书”或已登记域名的外链 |
| 组类 | `groups/` | 分期组类、分布、是否组类限定。未知写 `unknown` |
| 辞例 | `transcriptions/` 与 `dual-entries/` | 自录释文。双人各写一份 |

`records/` 放档位和流程状态，不放图像。`crosswalk/` 放和字书或数据集字头的对应，可空。不沿用 HUST-OBC 等数据集的编号。

`OBD-900001` 至 `OBD-900099` 是测试编号段，永不发给真实字形。演练日志放在 `pilot/_drill/`。

当前三件样例都标了“示例数据，非真实释读”，著录号是虚构的 `示例字编EX-*`。

Schema 在 `schema/`。规则常量在 `policy.json`。其中的天数和次数是经验设定，待校准。

## English

Three layers, one opaque id. The range OBD-900001 through OBD-900099 is reserved for drills and is never issued for a real graph. Sample files are fictional.
