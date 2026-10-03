# 来源调查（2026-10-04）

这是阶段 2 的公开网页摸底，只记录本次实际打开或请求失败的页面。它不是释读，不登记真实字形，也不新发 OBD 编号。

[来源调查](source-survey-2026-10-02.md) 与 [可读来源调查](source-survey-2026-10-02-readable.md) 已记录：2026-10-02 没有在合法免费公开网页上找到《综理表》和《待问编》的全文。该结论先合并在拉取请求 [#4](https://github.com/horizoncove/oracle-bone-decipher/pull/4)。本次不重开。下面找的是不必依赖那两部全文、仍可能用来挑选试点字的页面。

`research/` 里的工作笔记不作为本文件的证据。

## 检索

- 检索日：2026-10-04（Asia/Shanghai）。
- 做法：打开下表写明“已打开”的页面，或记录连接失败。没有登录，没有去图书馆，没有下载网盘、图像、权重、数据集或电子书。字形若在页面上是图片，不下载、不裁切、不保存，也不把图片地址写进本仓库。
- 检索摘要里出现的期刊付费页、电子书下载页和网盘页没有打开，下面不给链接。
- `login_required` 只写本次所见：不必提交口令就读到正文，写“否”；页面没有返回，写“未核实”。试点日志本身只接受“是”或“否”。

## 复旦出土文献与古文字研究中心站内检索

检索框提交到 `https://www.fdgwz.org.cn/Web/Search`，参数 `s`。下列结果页都是 HTTP 200，基本浏览无需登录。结果是篇名列表，不是字表。篇名列表本身不能用来挑选试点字。本次只打开了下面“文章正文”一节里写出的篇目。

| 检索词 | 结果页写明的条数 | 能否据此挑选试点字 |
| --- | --- | --- |
| 視為未識 | 1。篇名为阶段 1 已打开的王子扬文 | 否 |
| 未識字 | 23 | 否。只是篇名 |
| 未釋字 | 26 | 否 |
| 不識字 | 20 | 否 |
| 附錄上 | 12 | 否 |
| 入於附錄 | 3 | 否 |
| 收入附錄 | 10 | 否 |
| 新甲骨文編 | 70。本次只看到第一页篇名 | 否 |
| 待考 | 342。本次只看到第一页篇名 | 否 |
| 附錄0 | 0 | 否 |
| 视为未识（简体） | 0 | 否 |

新主机名仍是 `www.fdgwz.org.cn`。本次不加入 `registry/allowed-link-domains.txt`。等将来某条字形记录真要引用时再考虑。

## 文章正文

| 页面 | 本次 | login_required | 能否据此挑选试点字 |
| --- | --- | --- | --- |
| [黄天树：商代文字的构造与“二书”说（上）](https://www.fdgwz.org.cn/Web/Show/433)（页上发布日期 2008-05-12） | 已打开，HTTP 200 | 否 | 只作书目指针，见下一节。不登记真实字形 |
| [谢明文：释甲骨文中的“[八丏]”及相关诸字](https://www.fdgwz.org.cn/Web/Show/11009)（页上发布日期 2023-03-20） | 已打开，HTTP 200 | 否 | 只作书目指针，见下一节。不登记真实字形 |
| [金赫：甲骨文札记二则](https://www.fdgwz.org.cn/Web/Show/2778)（页上发布日期 2016-04-21） | 已打开，HTTP 200 | 否 | 否。见下 |
| [刘洪涛：说“争”、“静”是“耕”的本字](https://www.fdgwz.org.cn/Web/Show/1126)（页上发布日期 2010-04-09） | 已打开，HTTP 200 | 否 | 否。见下 |
| [刘钊：甲骨文“害”字及从“害”诸字考释](https://www.fdgwz.org.cn/Web/Show/2093)（页上发布日期 2013-08-11） | 已打开，HTTP 200 | 否 | 否。见下 |
| [杨泽生：甲骨文“椎”字考释](https://www.fdgwz.org.cn/Web/Show/696) | 已打开，HTTP 200 | 否 | 否。抽看写到《甲骨文编》附录上四二，是在讨论该文准备隶定的讹变，没有同时给出该书页码和一条仍作未识的片号 |
| [陈剑：说殷墟甲骨文中的“玉戚”](https://www.fdgwz.org.cn/Web/Show/902) | 已打开，HTTP 200 | 否 | 否。抽看所及的附录号在《金文编》 |
| [王宁：释福格藏玉戈铭文中的“香（享）”](https://www.fdgwz.org.cn/Web/Show/4282)（页上发布日期 2018-07-31） | 已打开，HTTP 200 | 否 | 否。页上的“附录上”是《金文编（四版）·附录上》375、第 1116 页，讨论金文。不转录铭文 |
| [李宗焜《甲骨文字编》出版说明](https://www.fdgwz.org.cn/Web/Show/1843) | 已打开，HTTP 200 | 否 | 否。说明该书改用自然分类，并说明旧《甲骨文编》附录难查。没有点名一个未识字的页码和片号 |

上表各文若提出释读，本调查都不采纳，也不转录辞例。字形在这些页上多是图片，没有保存。

金赫文写：《合》22055 之字，前人未释，大部分工具书作为未识字入于附录；注 [1] 写孙海波《甲骨文编》第 821 页（中华书局，1965 年）、李宗焜《甲骨文字编》第 1322 页（中华书局，2012 年）。同一页注 [2] 写刘钊等《新甲骨文编》（增订本）已把此字列入“乇”字条，第 384、1084 页（福建人民出版社，2014 年）。同页既写出后来的字编已立字头，就不能当作一条“字编仍作未识”的试点指针。不另立演练日志。

刘洪涛文写所谓“争”字见《甲骨文编·附录上》第 736 页，注 [2] 只给 1965 年中华书局书目。正文没有写出这一形的合集号。缺片号，不能挑选试点。不另立演练日志。

刘钊文写三个形体里的第一个，《甲骨文编》列于附录上一〇一；《甲骨文字编》把其中两形“作为不识字”，编号 1294 与 0320。这两句没有写出对应页码。同页又写《新甲骨文编》已把其中两形列在字头下。缺页码，且同页已写后来的字编立了字头，不另立演练日志。不转录该文辞例。

黄天树文是“（上）”篇。编辑说明写原文较长，拟分上中下三次发布。本次只打开了这一篇，没有打开中篇或下篇。

## 可以留给以后挑选的三条指针

三条都不必登录就能读到文字。都不进入 `registry/`，都不发给真实 OBD 编号。`www.fdgwz.org.cn` 与 `xiaoxue.iis.sinica.edu.tw` 本次不加入允许表。

1. [黄天树文](https://www.fdgwz.org.cn/Web/Show/433) 写明：所论之字，《甲骨文编》当作未释字收在附录里；注 [25] 写附录第 731 页、第 3768 号，中华书局，1965 年；同页把这条标为《合集》6528。指针写在 [`pilot/_drill/OBD-900003.md`](../pilot/_drill/OBD-900003.md)。同页注 [21] 另有附录第 4834 号，没有该书页码，缺页码不算证据，不另立指针。
2. [谢明文文](https://www.fdgwz.org.cn/Web/Show/11009) 写：《合》37504（《前》2·7·5）之字，《甲骨文编》入附录上一三〇；《集释》列入待考，页上作“四六一六页”。同页还写《合》36754。指针写在 [`pilot/_drill/OBD-900004.md`](../pilot/_drill/OBD-900004.md)。附录上一三〇在该句没有页码，证据条只用《集释》的页码。
3. 小学堂页码检索的一条结果，见下一节。指针写在 [`pilot/_drill/OBD-900005.md`](../pilot/_drill/OBD-900005.md)。

限制，必须一起保留：

- 上述页面上的字形是图片，或结果页的字头是图片。本仓库不下载、不裁切、不保存这些图片。
- 前两篇是考释。本调查不转写其辞例，也不采纳其释读。页上的“未释字”“待考”“入于附录”是作者对字编或集释处理的转述，不是本仓库对今天学界状况的判断。
- `OBD-900003` 至 `OBD-900005` 是保留测试号，只用来把非发布记录放在 `pilot/_drill/`。不写 `registry/`。
- 各日志的 `image_pointer` 只写书名和页码，不是图像文件，也不是图像链接。

## 小学堂甲骨文数据库

主机 `xiaoxue.iis.sinica.edu.tw` 本次不加入允许表。基本浏览无需登录。没有保存字形图片。

| 页面或请求 | 本次 | login_required | 调查所见 |
| --- | --- | --- | --- |
| [资料库首页](https://xiaoxue.iis.sinica.edu.tw/jiaguwen) | 已打开，HTTP 200 | 否 | 首页消息写本库共收字头 2548 个、字形 24701 个，并写日期 2026/10/4。检索表单在页面上，不必登录 |
| [凡例](https://xiaoxue.iis.sinica.edu.tw/jiaguwen/Example/Example) | 已打开，HTTP 200 | 否 | 写收录字头 1724 个、字形 18846 个；写目前所收字形仅限《甲骨文编》正编，未收录合文及附录字形 |
| [收录现况](https://xiaoxue.iis.sinica.edu.tw/jiaguwen/Statistics/Statistics) | 已打开，HTTP 200 | 否 | 表内“甲骨文编”一行写字头数 2548、字数 24701 |
| [简介](https://xiaoxue.iis.sinica.edu.tw/jiaguwen/About/About) | 已打开，HTTP 200 | 否 | 写字头一千七百多个、字形超过一万八千个；写收录以《甲骨文编》为主 |
| [使用说明页](https://xiaoxue.iis.sinica.edu.tw/jiaguwen/Help/Help) | 已打开，HTTP 200 | 否 | 只有两份简介文件的链接，说明正文不在这一页 |
| [使用简介 PDF](https://xiaoxue.iis.sinica.edu.tw/jiaguwen/Content/Files/jiaguwen-Get_Started.pdf) | 已打开，HTTP 200，24 页 | 否 | 写页码检索依据《甲骨文编》的页码；输入单一页码时，同一页若有两个以上字头，预设显示该页第一行的字头。写字号是正编字头编号 1–1723，1368B 改编为 1724。简介里的示例字是已有楷书字头的检索例子，不拿来当试点 |

凡例、简介、收录现况和首页消息对字头数的说法不一致。凡例写未收附录，首页和收录现况的数字又大于凡例所写的正编规模。本调查不裁定哪一说代表 2026-10-04 的库内范围，也不把某一次页码命中改写成“附录已经收录”。

按简介提交的页码检索（只读返回的文字，不保存图片）：

| 提交的页码 | 返回文字里能读到的著录 | 能否据此挑选试点字 |
| --- | --- | --- |
| 821 | 两条：前 4.5.5、合 14158、宾组；前 5.25.1、合 14157、宾组。相关索引写《甲骨文字编》字号.册页 0161.上54；《甲骨文字诂林》册.页 1.164；《甲骨文字集释》卷.页 待考.4620；《殷墟甲骨刻辞类纂》册页 上71 | 只把“待考.4620”加合集号当作书目指针，见 `OBD-900005`。0161.上54 那一行没有写未识或待考，不另立未识证据。字头是图片，不转写 |
| 731 与 731.1 | 各返回一条：甲 2336、合 35269。返回文字里没有“待考”或“附录” | 否。黄天树文把《合集》6528 标在《甲骨文编》附录第 731 页。这次页码 731 的返回写的是合 35269，不是合 6528。两处不合并成一条 |
| 736 | 返回写“共搜寻到 31 字／2 页”。第一屏能读到的旧著录和合集号很多，包括铁 15.4、合 4009 等，直到合 6552。这一屏没有“待考”或“附录”字样。第二页没有再请求 | 否。刘洪涛文只给附录上第 736 页，没有片号。不从这 31 条里指定哪一条是该文所论之字 |

金赫文把《合》22055 的旧附录处理标在《甲骨文编》第 821 页。页码 821 的检索返回写的是合 14158 与合 14157。两处不合并成一个字。

## 其他打开或失败的页面

| 页面 | 本次 | login_required | 能否据此挑选试点字 |
| --- | --- | --- | --- |
| [殷契文渊](https://jgw.aynu.edu.cn/) 与 [jgw.aynu.edu.cn/home/](https://jgw.aynu.edu.cn/home/) | 各请求约 20 秒后超时，没有页面 | 未核实 | 否。与 2026-10-02 的记录相同，免登录可读性仍未核实 |
| [缀玉联珠甲骨缀合信息库](https://www.fdgwz.org.cn/ZhuiHeLab/Home) | 已打开，HTTP 200 | 否（仅这一简介页） | 否。简介写库内有缀合信息，免费使用。没有未识字头。本次没有在检索框提交片号，演练日志的缀合库查询日期仍写“未查询” |
| [李宗焜前言的另一网址](https://idv.sinica.edu.tw/lizk/2012D.htm) | HTTP 404 | 否 | 否。同文的出版说明已在上面的复旦页打开 |
| [甲骨文学术著作的入门书](https://epaper.gmw.cn/zhdsb/html/2019-06/05/nw.D110000zhdsb_20190605_2-15.htm)（中华读书报·光明网，版面路径日期 2019-06-05） | 已打开，HTTP 200 | 否 | 否。文中把《甲骨文编》附录上七〇与《卜辞通纂》第 426 片说成后来已可读的“明”，并写出《合集》13442 正、16057。这是在说一个后来被收进常用字的例子，不是一条仍作未识的指针。同页提到“甲骨文已识字、有争议字和未识字综理表”作为一部字典的资助课题名称，没有给出该表正文。这不重开 2026-10-02 对全文的否定结论 |
| [河南省文物局的同题转载](https://wwj.henan.gov.cn/2024/11-08/3083694.html) | 请求超时，没有页面 | 未核实 | 否 |
| `https://www.wzbwg.com/search?keyword=500` | 已打开，HTTP 200 | 否 | 否。返回的是中国文字博物馆首页，正文没有“未释”。没有找到第一批 500 个未释读字形的字表 |

阶段 1 已经打开的中新网新闻仍然是“将要发布 500 个字形”，本次没有再打开那篇。本次也没有找到这份字表。

## 没有写成指针的原因

可以挑选试点字，需要同一页同时给出：字编或集释把它当作未识或待考、页码、以及合集或其他著录号。缺页码不算证据。同页若写明后来的《新甲骨文编》已经把该形列入已有字头，本次不把该形再写成“仍作未识”的演练指针。考释文章里的释读一律不采纳。

因此本次没有从金赫文、刘洪涛文、刘钊文，以及小学堂页码 731、736 的返回里新立指针。

## 引用时的限制

只使用合法公开来源。不上传图像，不粘贴未授权的书页、释文或字表。缺页码的条目不算证据。本调查文件没有结论等级。三条演练日志的 `conclusion_level` 都是“线索待查”。

新出现的主机名 `www.fdgwz.org.cn`、`xiaoxue.iis.sinica.edu.tw`、`epaper.gmw.cn`、`idv.sinica.edu.tw`、`wwj.henan.gov.cn` 本次不加入允许表。`jgw.aynu.edu.cn` 与 `www.wzbwg.com` 本来就在允许表里。列入只表示域名已登记，不等于可以复制图像或正文。

## English

Search date: 2026-10-04 (Asia/Shanghai). This file records pages that were opened or that failed to connect. It is not a decipherment and it registers no glyph. The 2026-10-02 finding that no legal public full text of 综理表 or 待问编 was found is not reopened. Notes under `research/` are not evidence.

Three bibliographic pointers use reserved drill ids. Huang Tianshu’s 2008 essay on the Fudan center site says *Jiaguwen bian* treats the graph as unidentified in the appendix, note 25 gives appendix page 731 and number 3768, and the same page marks the inscription as *Heji* 6528 (`pilot/_drill/OBD-900003.md`). Xie Mingwen’s 2023 essay says the graph on *Heji* 37504 (*Qian* 2.7.5) is *Jiaguwen bian* appendix 上130 and that *Jishi* places it under 待考 at the page written 四六一六 (`OBD-900004.md`). A login-free query of the Academia Sinica Xiaoxuetang oracle-bone database, page number 821, returned a related-index line “甲骨文字集释, 待考.4620” together with *Heji* 14158 and *Heji* 14157 (`OBD-900005.md`). The database help PDF says a single page number shows the first head on that *Jiaguwen bian* page. None of these files adopts a reading or transcribes an inscription. Glyphs on the pages are images and were not saved. `image_pointer` names the book and page only. The new hostnames stay off the allowlist because no registry record cites them.

Other opened pages do not support choosing a pilot. Jin He’s essay gives *Jiaguwen bian* page 821 and *Jiagu wenzi bian* page 1322 for *Heji* 22055, then says the revised *Xin jiaguwen bian* already files the graph under 乇. Liu Hongtao’s essay gives *Jiaguwen bian* appendix page 736 and no collection number. Liu Zhao’s essay gives appendix 上101 and two *Jiagu wenzi bian* serials without pages, and says *Xin jiaguwen bian* already files two of the forms under a head. A Xiaoxuetang query for page 731 returned *Heji* 35269, which is not the *Heji* 6528 named by Huang, so the two are not merged. A query for page 736 returned many collection numbers and no 待考 label; it is not matched to Liu Hongtao’s page. The Xiaoxuetang 凡例 still says appendix graphs are excluded, while the statistics page and the homepage give a larger head count. This survey does not resolve that disagreement.

Yinqi Wenyuan (`jgw.aynu.edu.cn`) timed out again, so browsing without login stays unverified. The Fudan rejoining-database homepage is readable and names no unidentified graph; no rejoining query was submitted. A Guangming Daily book essay discusses an appendix graph as later read 明 and mentions 综理表 only as a funded project’s name, without the table’s text. A Henan provincial page timed out. A museum search URL returned the museum homepage and no list of 500 graphs. HUST-OBC, Oracle-50K, and OBC306 stay out of the tree.
