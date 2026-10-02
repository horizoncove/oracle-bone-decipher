import sys, re, subprocess, collections, urllib.parse, html
def fetch(ch, page=1):
    d = urllib.parse.urlencode({"EudcFontChar":ch,"PaginalZiNum":"50","ImageSize":"36","PageNo":"","Page":str(page)})
    return subprocess.run(["curl","-sL","-m","40","-A","Mozilla/5.0","-H","X-Requested-With: XMLHttpRequest","-X","POST","-d",d,
      "https://xiaoxue.iis.sinica.edu.tw/jiaguwen/PageResult/PageResult"],capture_output=True,text=True).stdout
for ch in sys.argv[1:]:
    h = fetch(ch); open(f"raw/xxt_{ch}.html","w").write(h)
    tot = re.search(r'共搜尋到(\d+)字／(\d+)頁', re.sub('<[^>]+>','',h))
    kai = sorted(set(re.findall(r'kaiOrder=(\d+)', h)))
    items = re.findall(r'class="VariantList[AB]"><img[^>]*/><br />([^<]*)<br />([^<]*)<br />((?:<img[^>]*/>)?[^<]*)<td>', h)
    items = [(a,b,re.sub(r'<img[^>]*/>','𠂤',c)) for a,b,c in items]  # 𠂤組 的𠂤是图片
    cats = collections.Counter(c or '（無）' for _,_,c in items)
    hj = [b for _,b,_ in items if b]
    print(f"## {ch}: 字頭數/頁={tot.groups() if tot else None} kaiOrder={kai} 字形數(本頁)={len(items)}")
    print("  類組:", dict(cats))
    print("  合集:", " ".join(hj))
    print("  全部:", " ; ".join("|".join(x) for x in items))
