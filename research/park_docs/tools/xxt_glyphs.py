# usage: xxt_glyphs.py out.png 字1 字2 ...  -> downloads 小学堂 glyph images (size 72) with 著录|合集|类组 labels
import sys,re,subprocess,urllib.parse,io,html,os
from PIL import Image,ImageDraw,ImageFont
F='/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc'; f=ImageFont.truetype(F,11); fb=ImageFont.truetype(F,16)
B='https://xiaoxue.iis.sinica.edu.tw'
def post(ch,page):
    d=urllib.parse.urlencode({"EudcFontChar":ch,"PaginalZiNum":"50","ImageSize":"72","PageNo":"","Page":str(page)})
    return subprocess.run(["curl","-sL","-m","40","-A","Mozilla/5.0","-H","X-Requested-With: XMLHttpRequest","-X","POST","-d",d,B+"/jiaguwen/PageResult/PageResult"],capture_output=True,text=True).stdout
blocks=[]
for ch in sys.argv[2:]:
    h=post(ch,1); os.makedirs('raw',exist_ok=True); open(f'raw/xxt72_{ch}.html','w').write(h)
    items=re.findall(r'class="VariantList[AB]"><img src="([^"]*)"[^>]*/><br />([^<]*)<br />([^<]*)<br />((?:<img[^>]*/>)?[^<]*)<td>',h)
    items=[(s_,a,b,re.sub(r'<img[^>]*/>','𠂤',c)) for s_,a,b,c in items]
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(12) as ex: pngs=list(ex.map(lambda it: subprocess.run(["curl","-sL","-m","30","-A","Mozilla/5.0",B+html.unescape(it[0])],capture_output=True).stdout, items))
    T=80; cols=10; rows=max(1,(len(items)+cols-1)//cols)
    Bk=Image.new('RGB',(cols*(T+50)+4,26+rows*(T+30)),'white'); d=ImageDraw.Draw(Bk); d.text((4,2),f"小学堂 {ch} n={len(items)}",font=fb,fill='black')
    for i,(src,a,b,c) in enumerate(items):
        png=pngs[i]
        try:
            im0=Image.open(io.BytesIO(png)).convert('RGBA'); im=Image.new('RGB',im0.size,'white'); im.paste(im0,mask=im0.split()[3]); im.thumbnail((T,T))
        except Exception: im=Image.new('RGB',(T,T),'pink')
        x=4+(i%cols)*(T+50); y=26+(i//cols)*(T+30); Bk.paste(im,(x,y))
        d.text((x,y+T),f"{b or a}",font=f,fill='blue'); d.text((x,y+T+13),c,font=f,fill='green')
    blocks.append(Bk)
W=max(b.width for b in blocks); S=Image.new('RGB',(W,sum(b.height for b in blocks)),'white'); y=0
for b in blocks: S.paste(b,(0,y)); y+=b.height
S.save(sys.argv[1]); print(sys.argv[1],S.size)
