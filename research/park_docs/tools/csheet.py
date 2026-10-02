# usage: csheet.py out.png cols label1=dir_or_glob [label2=...]  (labels each file with index)
import sys,glob,os
from PIL import Image,ImageDraw,ImageFont
F='/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc'
f=ImageFont.truetype(F,12); fb=ImageFont.truetype(F,18)
out=sys.argv[1]; cols=int(sys.argv[2]); T=110
blocks=[]
for a in sys.argv[3:]:
    lab,pat=a.split('=',1)
    fs=sorted(glob.glob(pat+'/*.png') if os.path.isdir(pat) else glob.glob(pat), key=lambda p:[(0,int(t),'') if t.isdigit() else (1,0,t) for t in os.path.basename(p).replace('.','_').split('_')])
    if os.environ.get('MAXN'): fs=fs[:int(os.environ['MAXN'])]
    rows=(len(fs)+cols-1)//cols
    B=Image.new('RGB',(cols*(T+4)+4,30+rows*(T+18)),'white'); d=ImageDraw.Draw(B); d.text((4,4),f"{lab} (n={len(fs)})",font=fb,fill='black')
    for i,p in enumerate(fs):
        im=Image.open(p).convert('RGB'); im.thumbnail((T,T)); x=4+(i%cols)*(T+4); y=30+(i//cols)*(T+18)
        B.paste(im,(x+(T-im.width)//2,y+(T-im.height)//2)); d.rectangle([x,y,x+T-1,y+T-1],outline='#aaa')
        n=os.path.basename(p)[:-4]; d.text((x,y+T),f"{i}:{n[-14:]}",font=f,fill='blue')
    blocks.append(B)
W=max(b.width for b in blocks); S=Image.new('RGB',(W,sum(b.height for b in blocks)),'white'); y=0
for b in blocks: S.paste(b,(0,y)); y+=b.height
S.save(out); print(out,S.size)
