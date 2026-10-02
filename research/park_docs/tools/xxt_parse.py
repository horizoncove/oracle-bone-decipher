# parse raw/xxtzi_*.html -> raw/xxt_index.json: zi, n, kai (楷书 img alts), idx dict, items [(旧著录,合集,类组)]
import re,glob,json,os,html
out=[]
for p in glob.glob('raw/xxtzi_*.html'):
    z=int(re.search(r'_(\d+)\.html',p).group(1)); h=open(p,encoding='utf8',errors='replace').read()
    if 'StartOrder' not in h: continue
    line=re.search(r'StartOrder">\d+</span></td>\s*<td>(.*?)</td>',h,re.S)
    kai=re.findall(r'text=([^&]*)&(?:amp;)?font=([^&]*)',line.group(1)) if line else []
    import urllib.parse as U
    kai=''.join(U.unquote(t) if '部件外字' not in U.unquote(f) and '小篆' not in U.unquote(f) else '□' for t,f in kai)
    items=re.findall(r'class="VariantList[AB]"><img[^>]*/><br />([^<]*)<br />([^<]*)<br />((?:<img[^>]*/>)?[^<]*)<td>',h)
    items=[(a,b,re.sub(r'<img[^>]*/>','𠂤',c)) for a,b,c in items]
    tot=re.search(r'共搜尋到(\d+)字',h)
    idx=dict(re.findall(r'(甲骨文編|新甲骨文編|殷墟甲骨刻辭類纂|甲骨文字詁林|甲骨文字集釋)（[^）]*），[^：]*：\s*([^\s<]+)',h))
    out.append(dict(zi=z,kai=kai,n=int(tot.group(1)) if tot else 0,idx=idx,items=items))
out.sort(key=lambda r:r['zi']); json.dump(out,open('raw/xxt_index.json','w'),ensure_ascii=False)
print(len(out))
