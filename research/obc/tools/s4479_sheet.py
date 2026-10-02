import json
from PIL import Image,ImageDraw,ImageFont,ImageOps
OB='/workspace/obimd'; FONT='/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
d={r['RubbingName']:r for r in json.load(open(OB+'/data.json'))}
m=json.load(open(OB+'/Main-character.json'))
items=[('H4479','a7al7kr0c5','a7al 合4479「壬辰卜叀□令」'),('H30442','a7al7kr0c5','a7al 合30442「…卜□…□…王賓…」'),
('H14660','gaf7rmekoj','T9 合14660「…亥卜尞于□𰇑二牛」'),('H14666','gaf7rmekoj','T9 合14666「乙卯卜㱿貞尞于□」'),
('H14650','gaf7rmekoj','T9 合14650「□羊㞢豚」'),('H14679','gaf7rmekoj','T9 合14679「貞□…雨」'),('H1508','gaf7rmekoj','T9 合1508「貞于□㞢」')]
H=330; f=ImageFont.truetype(FONT,22); fs=ImageFont.truetype(FONT,15)
rows=[]
for rn,lab,cap in items:
    r=d[rn]; box=None
    for g in r['RecordUtilSentenceGroupVoList']:
        for c in g['RecordUtilOracleCharVoList']:
            if c['Label']==lab and box is None: box=list(map(int,c['Position'].split(',')))
    x,y,w,h=box; p=10
    rub=Image.open(OB+'/'+r['Rubbing']).convert('L'); fac=Image.open(OB+'/'+r['Facsimile']).convert('L')
    cr=(max(0,x-p),max(0,y-p),x+w+p,y+h+p)
    def up(im): s=H/im.height; return im.resize((int(im.width*s),H),Image.LANCZOS)
    a=up(rub.crop(cr)); b=up(ImageOps.invert(ImageOps.autocontrast(rub.crop(cr),cutoff=2))); c_=up(fac.crop(cr))
    ctx=rub.convert('RGB'); dd=ImageDraw.Draw(ctx); dd.rectangle((x,y,x+w,y+h),outline=(255,0,0),width=3)
    ctx=up(ctx)
    rows.append((cap,f'{w}×{h}px 原图{rub.size[0]}×{rub.size[1]}',[ctx,a,b,c_]))
W=max(1180,max(sum(im.width+12 for im in ims) for _,_,ims in rows)+20)
out=Image.new('RGB',(W,60+len(rows)*(H+50)),'white'); D=ImageDraw.Draw(out)
D.text((10,10),'a7al7kr0c5（合4479、30442）对 T9 gaf7rmekoj：全版｜拓片放大｜反相增强｜摹本　【未核：目验】',font=f,fill=0)
yy=60
for cap,sz,ims in rows:
    D.text((10,yy),cap+'　'+sz,font=fs,fill=0); xx=10
    for im in ims: out.paste(im,(xx,yy+22)); xx+=im.width+12
    yy+=H+50
out.save('/workspace/obc/h4479_vs_t9.png'); print(out.size)
