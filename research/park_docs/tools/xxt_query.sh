#!/bin/bash
# 小学堂甲骨文: 按字头(楷书)查字形+舊著錄+合集號+類組; 可加合集號/類組做过滤(不能单独按合集號查)
# 用法: xxt_query.sh 字 [合集號,逗号分隔]
curl -sL -m 30 -A "Mozilla/5.0" -H "X-Requested-With: XMLHttpRequest" -X POST \
 --data-urlencode "EudcFontChar=$1" --data-urlencode "HeJiOrder=$2" -d "PaginalZiNum=50&ImageSize=36" \
 https://xiaoxue.iis.sinica.edu.tw/jiaguwen/PageResult/PageResult \
 | grep -oE '<br />[^<]*<br />(合[^<]*)?<br />[^<]*<td>' | sed 's/<br \/>/|/g;s/<td>//'
