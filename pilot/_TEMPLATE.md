---
glyph_id: ""
tier: ""
origin_source: "待确认"
corpus_scope: ""
started: ""
last_updated: ""
researcher: ""
conclusion_level: "证据不足暂不结论"
public: false
second_reviewer: ""
missed_attestation_in_batch: false
changelog: []
evidence: []
---

# 试点研究日志模板

本模板不填任何真实字。复制后再填写。演练请放到 `pilot/_drill/`，并且只能使用测试编号 OBD-900001 至 OBD-900099。该目录会参与校验，但不进入数据发布和统计。

甲骨文存在“一形多用”，只比字形不够，要先看用法。

`corpus_scope` 在开始检索后必填，写三件事：查过的著录书简称列表、ISO 检索日期（`YYYY-MM-DD`）、缀合库查询日期（`YYYY-MM-DD`）。示例（仍是虚构格式，不要当成真实检索）：`示例字编；检索日期 2026-10-02；缀合库查询日期 2026-10-02`。留空时，`conclusion_level` 最高只能到“线索待查”。

降档时保留旧记录，不要删改历史。每次更新在 `changelog` 追加一行，并在正文“变更说明”写同一句。等级为“候选假说”或“候选假说有争议”时，须另一名研究者复核后才能把 `public` 设为 true。同一批著录里发现漏掉辞例，则 `missed_attestation_in_batch` 为 true，结论降为“线索待查”，直到补全。

没有“已破译”这一档。

## 证据清单

每条写在文首 `evidence` 列表里，不要只写在正文。字段是：著录号 `catalog_ref`、辞例原文 `quotation`、出处 `source`、页码 `page`、核对人 `checker`、是否需登录 `login_required`。是否需登录只能填“是”或“否”。

缺页码的条目不算证据。不要在这里粘贴图像。

选“是”的出处只能作个人线索。别人无法免登录复核，这和“证据必须可核查”冲突。日志里只要有一条选“是”，`conclusion_level` 最高到“线索待查”。

虚构格式，不要当成真实检索：

```yaml
- catalog_ref: "示例字编EX-9"
  quotation: "示例辞，非真实"
  source: "示例数据库"
  page: "12"
  checker: "example-checker"
  login_required: "否"
```

## 已排除的假说

写排除理由和出处。没有则写“无”。

## 反证与回应

逐条记录。没有则写“无”。

## AI 线索

不计入证据。若引用模型输出，只可转写其指针与 `machine-suggestion` 标识，不能写入证据清单。

## 当前结论与升级条件

默认：证据不足暂不结论。写明要升级到下一档还缺什么。

## 变更说明

每次更新追加一行。降档保留既有记录。

English: this blank template is not a real reading. `corpus_scope` must later list the catalogues consulted, an ISO search date, and the date the rejoining corpus was queried. Each evidence source has “是否需登录”. A “是” / yes is only a personal clue, and the log cannot rise above “线索待查”, because other people cannot check it without logging in. Oracle-bone graphs can share a shape and still differ in use; compare usage before shape. There is no status meaning “deciphered.”
