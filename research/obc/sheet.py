import json
from PIL import Image,ImageDraw,ImageFont
r=json.load(open('raw_results_top5.json'))
F='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
import os
if not os.path.exists(F): F='/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc'
f=ImageFont.truetype(F,18); fs=ImageFont.truetype(F,14)
T=150;LW=170;H=T+50
def tile(p):
    im=Image.open(p).convert('RGB'); im.thumbnail((T,T)); n=Image.new('RGB',(T,T),'white'); n.paste(im,((T-im.width)//2,(T-im.height)//2)); return n
rows=[]
for x in r:
    W=LW+7*(T+8)+20; row=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(row)
    d.text((6,10),x['cls'],font=f,fill='black'); d.text((6,40),f"n={x['n']}",font=fs,fill='black')
    d.text((6,62),"未释字 samples →",font=fs,fill='gray')
    for i,p in enumerate(x['samp']):
        X=LW+i*(T+8); row.paste(tile(p),(X,4)); d.rectangle([X,4,X+T-1,4+T-1],outline='#888')
        d.text((X,T+8),'sample',font=fs,fill='gray')
    X0=LW+3*(T+8)+20; d.line([X0-12,0,X0-12,H],fill='red',width=2)
    for i,(a,p) in enumerate(zip(x['A'][:3],x['ex'])):
        X=X0+i*(T+8); row.paste(tile(p),(X,4)); d.rectangle([X,4,X+T-1,4+T-1],outline='#3a3')
        d.text((X,T+8),f"#{i+1} {a[0]} p={a[2]:.2f}",font=f,fill='darkgreen'); d.text((X,T+30),f"HUST id {a[1]}",font=fs,fill='gray')
    rows.append(row)
    row.save(f"strips/{x['cls'].replace('/','_').replace('+','')}.png")
W=max(r_.width for r_ in rows); hdr=60
S=Image.new('RGB',(W,hdr+sum(r_.height for r_ in rows)+10*len(rows)),'white'); d=ImageDraw.Draw(S)
d.text((10,8),"HUST-OBC 未释字候选 v0.1 — left: 3 undeciphered samples; right: top-3 deciphered candidate exemplars (ResNet50 classifier, mean softmax p). AI candidates only, unverified. CC BY-NC 4.0 – internal use only.",font=fs,fill='black')
d.text((10,30),"Exemplar = deciphered image of that candidate class with highest MoCo-embedding similarity to the query set.",font=fs,fill='gray')
y=hdr
for r_ in rows: S.paste(r_,(0,y)); y+=r_.height; d.line([0,y+4,W,y+4],fill='#ccc'); y+=10
S.save('contact_sheet.png'); print(S.size)
