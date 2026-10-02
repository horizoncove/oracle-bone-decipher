# 可读来源调查（2026-10-02）

这是阶段 1 的另一次公开网页摸底，只记录本次实际打开或请求的页面。它不是释读，不登记真实字形，也不新发 OBD 编号。

[来源调查](source-survey-2026-10-02.md) 已记录：2026-10-02 没有在合法免费公开网页上找到《综理表》和《待问编》的全文。该结论先写在草稿拉取请求 [#2](https://github.com/horizoncove/oracle-bone-decipher/pull/2)。本次不重开。下面找的是不必依赖那两部全文、仍可能用来挑选试点字的页面。

`research/` 里的工作笔记不作为本文件的证据。

## 检索

- 检索日：2026-10-02。
- 做法：打开下表写明“已打开”的页面，或记录连接失败。没有登录，没有下载网盘、图像、权重、数据集或电子书。
- `login_required` 只写本次所见：不必提交口令就读到正文，写“否”；页面没有返回，或返回的只是没有字头的空壳，写“未核实”。试点日志本身只接受“是”或“否”；未核实的来源在有人免登录读到可引用文字之前，不能当作可复核证据。

## 打开结果

| 页面 | 本次 | login_required | 能否据此挑选试点字 |
| --- | --- | --- | --- |
| [王子扬：释甲骨文从“戈”之“祼”](https://www.fdgwz.org.cn/Web/Show/1578)（复旦大学出土文献与古文字研究中心，页上发布日期 2011-07-04） | 已打开，HTTP 200。合并记录时再次打开，仍可读 | 否 | 只作书目指针，见下一节。不登记真实字形 |
| [袁伦强：《新甲骨文编·附录》（增订本）校笺](https://www.fdgwz.org.cn/Web/Show/2903)（同站，页上发布日期 2016-09-22） | 已打开，HTTP 200 | 否 | 否。正文能读，但不是一份仍未识字的清单 |
| [首批甲骨文释读优秀成果获奖名单](https://www.wzbwg.com/newsinfo/320)（中国文字博物馆，页上日期 2018-06-11） | 已打开，HTTP 200 | 否 | 否。只有获奖篇名，没有未释字形 |
| [第二批甲骨文释读优秀成果获奖名单](https://www.wzbwg.com/newsinfo/11651)（中国文字博物馆，页上日期 2024-01-10） | 已打开，HTTP 200 | 否 | 否。同上 |
| [奖10万！500个未释读甲骨单字等你来“破”](https://www.chinanews.com.cn/cul/2022/12-27/9922421.shtml)（中国新闻网，2022-12-27） | 已打开，HTTP 200 | 否 | 否。新闻说将发布第一批 500 个字形，这篇正文没有列出这 500 个字 |
| [殷契文渊](https://jgw.aynu.edu.cn/) 与 [jgw.aynu.edu.cn/home/](https://jgw.aynu.edu.cn/home/)；另试过 `http://jgw.aynu.edu.cn/` | 连接超时，没有页面。合并记录时再请求首页与 `/home/`，各约 20 秒后仍超时 | 未核实 | 否 |
| [甲骨文 AI 协同平台](https://www.jgwlbq.org.cn/home) | 已打开，HTTP 200 | 未核实 | 否。返回的 HTML 是空的前端壳，并引用微信登录脚本；壳里没有字头 |
| [OBSD arXiv 摘要](https://arxiv.org/abs/2406.00684) | 已打开，HTTP 200 | 否 | 否。摘要没有点名一个未释字 |
| [OBSD ACL Anthology 页](https://aclanthology.org/2024.acl-long.831/) | 已打开，HTTP 200 | 否 | 否。摘要没有点名一个未释字 |
| [HUST-OBC arXiv 摘要](https://arxiv.org/abs/2401.15365) | 已打开，HTTP 200 | 否 | 否。摘要只给数量：1588 个已释字、9411 个未释字的图像，没有点名一个字头 |

新主机名 `www.fdgwz.org.cn`、`www.chinanews.com.cn`、`www.jgwlbq.org.cn` 本次不加入 `registry/allowed-link-domains.txt`。等将来某条字形记录真要引用时再考虑。`arxiv.org`、`aclanthology.org`、`github.com`、`www.wzbwg.com`、`jgw.aynu.edu.cn` 本来就在允许表里。列入只表示域名已登记，不等于可以复制图像或正文。

## 可以留给以后挑选的一条指针

[王子扬文](https://www.fdgwz.org.cn/Web/Show/1578) 不必登录就能读到正文。正文写明：所论之字在《新甲骨文编》中入“附录”0771 号（第 958 页），视为未识字；同一处指出《合》30945、《合》30946，并写《合》30946（安明 1688 清晰）。这足以做一条书目指针，而不必编造字形。指针写在 [`pilot/_drill/OBD-900002.md`](../pilot/_drill/OBD-900002.md)。

限制，必须一起保留：

- 字形在该页是图片。本仓库不下载、不裁切、不保存这些图片。
- 该文是考释。本调查不转写其辞例，也不采纳其释读。页上的“未识字”是作者对《新甲骨文编》处理的转述，不是本仓库对今天学界状况的判断。
- `OBD-900002` 是保留测试号，只用来把非发布记录放在 `pilot/_drill/`。它不发给这个字形。不写 `registry/`，不新发真实 OBD 编号。
- 该日志的 `image_pointer` 只写《新甲骨文编》附录 0771、第 958 页，不是图像文件，也不是图像链接。复旦网网址只出现在出处栏。登记记录没有引用 `www.fdgwz.org.cn`，所以本次不把该主机名加入允许表。以后若登记记录要引用它，再考虑列入，并且仍然不能放宽图像规则。

[校笺](https://www.fdgwz.org.cn/Web/Show/2903) 的开篇写《新甲骨文编》（增订本）附录收 1244 组字形，随后是分条校订。抽看的条目是在论证附录中的形应归入已识字，字形同样在图片里。因此它不能当作一份仍未识字的可选清单。本文件不摘录那些辞例。

博物馆两则获奖名单和中新网那则新闻都没有给出可核对的未释字形。殷契文渊首页这次没有返回。`www.jgwlbq.org.cn` 的壳页没有字头。

## OBSD 与三个数据集

OBSD 仓库 URL 的复核写在 [tools/README.md](../tools/README.md)。本文件不保存权重或数据集。

HUST-OBC、Oracle-50K、OBC306 仍不入库。2026-10-02 对 [Pengjie-W/HUST-OBC](https://github.com/Pengjie-W/HUST-OBC) 和 [whhamber/Oracle-50K](https://github.com/whhamber/Oracle-50K) 只做了 HTTP 头检查，二者返回 200。它们本来就是 [docs/datasets.md](datasets.md) 里的公开项目页，下载脚本没有改。OBC306 那条殷契文渊下载页随该主机超时，仍未复核，继续“待确认，不使用”。HUST-OBC 摘要里的未释字是图像数量，不是可读字头；论文的非商业限制不变。

## 引用时的限制

只使用合法公开来源。不上传图像，不粘贴未授权的书页、释文或字表。缺页码的条目不算证据。本调查文件没有结论等级。

## English

Search date: 2026-10-02. This file records pages that were opened or that failed to connect. It is not a decipherment and it registers no glyph. Draft PR #2 already recorded that no legal public full text of 综理表 or 待问编 was found; that conclusion is not reopened.

One opened page is readable without login. Wang Ziyang’s 2011 essay on the Fudan center site says the graph under discussion is *Xin jiaguwen bian* appendix 0771, page 958, treated there as unidentified, and it names *Heji* 30945, *Heji* 30946, and *Anming* 1688. The same bibliographic pointer is in `pilot/_drill/OBD-900002.md`. That file uses a reserved test id, so it is not a real OBD id and it is excluded from publication. The graph on that page is an image, which this repository does not copy. `image_pointer` names the book and page only. The essay proposes a reading; this survey does not transcribe the inscriptions or adopt the reading. `www.fdgwz.org.cn` stays off the allowlist because no registry record cites it.

The other opened pages are a collation that reassigns appendix graphs to known characters, museum award titles, a news item that announces 500 graphs without listing them, two paper abstracts that give counts rather than a named graph, and an empty web-app shell. Yinqi Wenyuan (`jgw.aynu.edu.cn`) timed out, including a repeat request of the homepage and `/home/` while these notes were combined, so browsing without login stays unverified. Other new hostnames stay off the allowlist until a glyph record needs them. HUST-OBC, Oracle-50K, and OBC306 stay out of the tree.
