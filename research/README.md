# research/ — 甲骨文未释字 AI 辅助释读：研究底稿汇总 / Oracle-bone undeciphered-glyph research dump

> **状态 / Status：研究底稿，不是释读结论。** All content here is working material from 2026-10-02 (UTC+8). AI candidates are **unverified**. Markers such as 【未核】(not checked against original rubbings/books), 【推测】(conjecture), 【待核】/待核 (to be checked), 【未核/AI】 are kept exactly as in the source notes and must be read literally.
>
> 本目录**不参与** `registry/` 的登记、状态与统计；这里的任何判断都不改变登记状态。Nothing in `research/` is a registry record; it does not change any glyph status.

## 1. 目录 / Layout

| 路径 Path | 内容 Content |
|---|---|
| [notion_20_candidates.md](notion_20_candidates.md) | Notion 页《未释字候选样例 v0.1（20 字）》导出：20 类候选总表（分类器 top-5、MoCo kNN top-5、异体/新字、字形系联、音义、出处、误刻排除）+ 按日期的各批结论与更正。Export of the Notion master page: 20-candidate table and dated conclusions/corrections. **Most up-to-date summary — start here.** |
| [obc/](obc/) | Grok Bot 的计算与分批报告（HUST-OBC 未释类）。Model runs and batch reports. |
| [park_docs/](park_docs/) | Loop Park 的 01–12 号核对文档（第 1/3/4 步：真伪、辞例、类组）与辞例表 CSV、对照图、脚本。Park's docs 01–12, inscription-example tables, figures, scripts. |
| [master_step6/](master_step6/) | Master 的第 6 步（跨材料：金文/小学堂字形）素材：茍/苟/敬/索/素/𦅽 字形截图与检索结果页。Master's step-6 cross-material notes (bronze/xiaoxue glyph captures). |

### 1.1 `obc/`
- `step25_batch1.md` … `step25_batch5.md` — 第 2、5 步（字形系联 / 音义）五批报告。Steps 2 & 5 batch reports.
  - batch1：X/2190、X/1814、X/2109、X/1485、X/2213；batch2：X/1401、X/2230、X/1366、X/1370、X/1850；batch3：X/276、X/1401（附 X/1212）；batch4：X/1190、X/839、X/365；batch5：X/462、X/956、X/849。
- `step2_x276_t9.md` — X/276 与史语所 Ｔ９ 对应复核（结论：同字【未核】部分见文内）。
- `results.md` / `results.csv` / `results_rows.json` / `raw_results*.json` — 20 类模型结果（ResNet50 分类器 + MoCo kNN）。Model outputs for the 20 classes.
- `limits.md` — 方法与局限 / methods & limits.
- `appendix_pool.md|csv`, `appendix_all_classes.csv`, `appendix_map.json`, `appendix_raw.json`, `x_classes_n.json` — 附录（真未释池）1224 类的映射与样本数。Appendix (truly-undeciphered pool) mapping.
- `notion_*.md`, `notion_step25.json`, `group_msg_batch*.md` — 写入 Notion / 群消息前的草稿（与 notion_20_candidates.md 内容重叠）。Drafts that were posted to Notion/group.
- `run*.py`, `build.py`, `mkpool.py`, `sheet.py`, `fs.py`, `fsdl.py`, `tools/*.py`, `run*.log` — 脚本与运行日志（依赖下文需另行下载的数据集与权重；`fsdl.py` 中 figshare 私链 key 已打码）。Scripts/logs; they expect the datasets/weights below at paths like `data/`, `HUST-OBS/`, `weights/` (not included).
- `figures/` — 我们制作的小型对照图（x*_sheet、*_vs_*、h* 拓片对照等）；`figures/step25_sheets/` 为第 2、5 步对照拼图。报告里写作 `/workspace/obc/xxx.png` 或 `step25_sheets/...` 的图，在此目录下同名。Small comparison figures we made; reports cite them by bare filename or `/workspace/obc/...` — look under `figures/`.

### 1.2 `park_docs/`
- `01` 辞例核对流程与数据源调研；`02` 途/烄/求；`03` 第二批 + `03-screen-…csv`（X 正编未释 vs 小学堂字头筛查表）；`04` 附录 TOP8；`05` 兆序重叠复核 X/297、X/839；`06` X/276、X/956、X/1370、X/1401；`06a` 合23248 误合核查；`07` X/297 结案稿；`08` 附录池配片号；`09` 旧释源（X/276 茍、X/1401 正编）；`10` 附录类对甲骨文编附录；`11` T9 神名辞例；`12` 年·雨·神类组对比（河·岳·夒·土·兇）。
- 辞例表 / inscription tables: `12-年雨神类组对比-逐条-v0.1.csv`, `…-逐条-v0.2.csv`（逐条辞例）, `12-年雨神类组对比-v0.1/v0.2.csv`, `12-年雨神两系对比-v0.2.csv`.
- `img/` 对照图，`tools/` 抓取/查询脚本，`screen/` 页码映射脚本与结果。
- 文中引用的 `raw/`（小学堂、史语所 lexdb、CDP 原始抓取，约 76 MB）与 `obimd/`（OBIMD 切图、嵌入 .pt）**未上传**；需要时按 `tools/` 脚本重抓或从 OBIMD 重建。`raw/` and `obimd/` referenced in the docs are **not included**.

### 1.3 `master_step6/`
- `gou_vs_x276.png`, `jinwen_gou_suo.png`, `jw2.png`, `jg_*.png`, `茍_*.png`, `索_*.png`, `素_*.png` — 甲骨/金文字形截图；`jg_*.html`, `jw_*.html` — 对应检索结果页存档；`u.txt` — 字形图片请求路径。

## 2. 当前结论摘要 / Current conclusions (2026-10-02, UTC+8)

以 `notion_20_candidates.md` 中带日期的小节为准；以下仅为索引，标记照抄原文。The dated sections in `notion_20_candidates.md` are authoritative.

- **X/276（附錄 7249–7251）＝ 史语所 Ｔ９ ＝《甲骨文编》附录 4418 ＝ OBIMD gaf7rmekoj，判为同字**（目验 + MoCo）【未核】；已有隶定“兇”（陈梦家，转引，页码未核）；神格待定；“茍”的推测**已撤回**；7252 仍定为“光”（误归）【未核】。合4479：近形待定、倾向同字【未核】；G282 ＝ T9 可能但未证实。T9 辞例以宾组、历组为主（park_docs/11）。
- **X/297**：宾组婦私名，隶定 [女糸]，写法与用法已定，读法待定（park_docs/07 结案稿；未对原拓与原书）。
- **X/1190 ＝ 璞，读撲（搏）**（旧释补证，连佳鹏 2019 转引）。
- **X/1189（书号 8143）**：新候选，方国或族名，宾组【未核】。
- **X/1401**：《新甲骨文编》正编约 249.3（幺部）已立字头，撤出新识候选；字形倾向索/𦅽一系【未核】。
- **X/839** 燕（重复著录，地名）；**X/365** 眉；**X/849** 祀（异体）；**X/462** 啟/肇待右旁；**X/956** 口/二覆丙（不是完整商）——均【未核/AI】。
- 第一批：X/2190 途、X/2109 求 可能性高（两法一致）；X/1814 烄；X/2213 酉彡（团队意见：酒/醻说见文献）；X/1485 未定。第二批五类均已在正编立字头，需翻原书抄隶定。
- 兆序误合筛查：H20717、H32512、HD451 降级；H23248 为“父”+ 兆序标注问题，非新字；HD180 待看整版。
- 方法事实：HUST-OBC X 子集流水号 ≥7091 为《新甲骨文编》附录段，共 1224 类 2009 张图，即“真未释池”（见 notion_20_candidates.md“真未释字池”节）。

## 3. 需另行下载的数据 / Datasets to download separately (not in this repo)

- **HUST-OBC**（含 HUST-OBS 分类器权重）：https://github.com/Pengjie-W/HUST-OBC ；figshare DOI 10.6084/m9.figshare.25040543（HUST-OBC.zip ≈ 608 MB）。**License: CC BY-NC 4.0（非商业）**。本目录只收少量我们自制的对照图，不再分发数据集图像。We do not redistribute the dataset; only a few small derived comparison figures are included.
- **OBIMD**（WAIC 2024 甲骨文多模态数据集）：Hugging Face dataset **KLOBIP/OBIMD** — https://huggingface.co/datasets/KLOBIP/OBIMD （CC BY 4.0，见数据集页）。

## 4. 排除项 / Excluded on purpose
HUST-OBC.zip、`data/`、`weights/`、`OBSD/`、`HUST-OBS/`、`gx/`、所有 `*.pt`、批量数据集样本条带（`strips/`、`app_strips/`、`contact_sheet.png`、`mont_strong.png`）、OBIMD 原始数据与切图、Park 的 `raw/` 原始抓取、第三方论文 PDF/HTML 全文（rits.pdf、ao_arxiv、yuan2903）。
