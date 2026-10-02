# 外部数据集

本仓库不收录这些数据。许可不明的一律标“待确认，不使用”。著录书释文能否录入，版权状态待确认。

| 名称 | 链接 | 许可 | 可商用 | 入库 |
| --- | --- | --- | --- | --- |
| HUST-OBC | 论文 [10.1038/s41597-024-03807-x](https://doi.org/10.1038/s41597-024-03807-x)；数据 [10.6084/m9.figshare.25040543.v3](https://doi.org/10.6084/m9.figshare.25040543.v3)；代码 [Pengjie-W/HUST-OBC](https://github.com/Pengjie-W/HUST-OBC)；ModelScope [wpj2003/HUST-OBC](https://www.modelscope.cn/datasets/wpj2003/HUST-OBC) | 论文写 CC BY-NC 4.0。Figshare 条目 API 的许可字段是 CC BY 4.0。两处不一致，待确认。在确认前按论文的非商业条款对待，只外链 | 按论文：否 | 否 |
| OBC306 | 论文页 [IEEE 8978032](https://ieeexplore.ieee.org/document/8978032)。一份综述 README 把下载页写成 `https://jgw.aynu.edu.cn/home/down/detail/index.html?sysid=16`。本仓库没有复核该页是否仍提供文件 | 待确认，不使用 | 待确认 | 否 |
| Oracle-50K | [whhamber/Oracle-50K](https://github.com/whhamber/Oracle-50K)。仓库根目录只有 README，GitHub 许可字段为空。README 写明来源包括 Xiaoxuetang、Koukotsu、Chinese Etymology | 待确认，不使用 | 待确认 | 否 |

下载脚本只允许把 HUST-OBC 放到被 git 忽略的 `data/downloads/`，而且要显式确认论文的非商业条款。见 [data/README.md](../data/README.md)。

字头编号不沿用这些数据集的编号。对应关系若要记，写在 `registry/crosswalk/`，可以留空。

## English

HUST-OBC stays outside the git tree. The paper says CC BY-NC 4.0; the Figshare metadata says CC BY 4.0. That conflict is unconfirmed. OBC306 and Oracle-50K are not used while their licenses are unknown.
