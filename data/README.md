# 数据目录

这里不存放甲骨文图像，也不存放 HUST-OBC、OBC306、Oracle-50K 的文件。

- `normalize.csv` 只有表头：`source_char,normalized_char,note`。它是兼容汉字到原字的占位表，待古文字研究员审定。校验会先按这张表替换，再做 NFC。
- `downloads/` 给本机下载用，已被 `.gitignore` 忽略。

```bash
python scripts/download_datasets.py --list
python scripts/download_datasets.py --dataset hust-obc --execute --acknowledge-paper-nc
```

第二行才会下载。OBC306 与 Oracle-50K 会被拒绝。

著录书里的释文能不能抄进登记，版权状态待确认。在确认之前，释文栏只放录入者自己的隶定，不粘贴书中整段原文。

## English

Do not commit datasets or images. The normalization table is an empty header until a paleographer reviews it. Whether published transcriptions may be copied is unconfirmed.
