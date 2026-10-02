# usage: xxt_zi.py out.png zi_from zi_to [maxglyph]  — scan 小学堂 by 甲骨文编字號 (ZiOrder); renders 楷书 + glyphs + 合集/类组; dumps raw/xxtzi_N.html and TSV
import sys,re,subprocess,urllib.parse,io,html,os,json
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageDraw,ImageFont
F='/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc'; f=ImageFont.truetype(F,11); fb=ImageFont.truetype(F,14)
B='https://xiaoxue.iis.sinica.edu.tw'
def curl(args,binary=False):
    r=subprocess.run(["curl","-sL","-m","60","-A","Mozilla/5.0"]+args,capture_output=True); return r.stdout if binary else r.stdout.decode('utf8','replace')
def getzi(z):
    p=f'raw/xxtzi_{z}.html'
    if os.path.exists(p) and os.path.getsize(p)>2000: return open(p).read()
    h=curl(["-H","X-Requested-With: XMLHttpRequest","-X","POST","-d",f"ZiOrder={z}&PaginalZiNum=50&ImageSize=36",B+"/jiaguwen/PageResult/PageResult"]); open(p,'w').write(h); return h
def img(src):
    try:
        im0=Image.open(io.BytesIO(curl([B+html.unescape(src)],True))).convert('RGBA'); im=Image.new('RGB',im0.size,'white'); im.paste(im0,mask=im0.split()[3]); return im
    except Exception: return Image.new('RGB',(30,30),'pink')
out,a,b=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]); MG=int(sys.argv[4]) if len(sys.argv)>4 else 12
zs=[int(t) for t in os.environ["ZL"].split(",")] if os.environ.get("ZL") else list(range(a,b+1))
with ThreadPoolExecutor(6) as ex: hs=list(ex.map(getzi,zs))
rows=[];tsv=[]
T=56
for z,h in zip(zs,hs):
    line=re.search(r'StartOrder">\d+</span></td>\s*<td>(.*?)</td>',h,re.S)
    kai=[s for s in re.findall(r'<img src="([^"]*)"',line.group(1))] if line else []
    items=re.findall(r'class="VariantList[AB]"><img src="([^"]*)"[^>]*/><br />([^<]*)<br />([^<]*)<br />((?:<img[^>]*/>)?[^<]*)<td>',h)
    items=[(s_,a,b,re.sub(r'<img[^>]*/>','𠂤',c)) for s_,a,b,c in items]
    tot=re.search(r'共搜尋到(\d+)字',h); idx=re.findall(r'(甲骨文編|新甲骨文編|殷墟甲骨刻辭類纂|甲骨文字詁林)（[^）]*），[^：]*：([0-9.A-Za-z\u4e00-\u9fff]+)',h)
    tsv.append(dict(zi=z,n=tot.group(1) if tot else '0',idx=dict(idx),items=[x[1:] for x in items]))
    with ThreadPoolExecutor(12) as ex: ims=list(ex.map(img,kai+[x[0] for x in items[:MG]]))
    R=Image.new('RGB',(150+MG*(T+44),T+34),'white'); d=ImageDraw.Draw(R)
    x=4
    for im in ims[:len(kai)]: im.thumbnail((40,40)); R.paste(im,(x,4)); x+=im.width
    d.text((4,46),f"#{z} n={tot.group(1) if tot else 0}",font=fb,fill='black'); d.text((4,64),f"新{dict(idx).get('新甲骨文編','-')}",font=f,fill='gray')
    for i,(im,it) in enumerate(zip(ims[len(kai):],items)):
        im.thumbnail((T,T)); X=150+i*(T+44); R.paste(im,(X,2)); d.text((X,T+4),it[2] or it[1],font=f,fill='blue'); d.text((X,T+17),it[3],font=f,fill='green')
    rows.append(R)
W=max(r.width for r in rows); S=Image.new('RGB',(W,sum(r.height for r in rows)),'white'); y=0
for r in rows: S.paste(r,(0,y)); y+=r.height; ImageDraw.Draw(S).line([0,y-1,W,y-1],fill='#ccc')
S.save(out); json.dump(tsv,open(out[:-4]+'.json','w'),ensure_ascii=False); print(out,S.size)
