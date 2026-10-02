import json
from PIL import Image,ImageDraw,ImageFont,ImageOps
OB='/workspace/obimd'; FONT='/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
d={r['RubbingName']:r for r in json.load(open(OB+'/data.json'))}
f=ImageFont.truetype(FONT,22); fs=ImageFont.truetype(FONT,15)
def box(rn,lab):
    for g in d[rn]['RecordUtilSentenceGroupVoList']:
        for c in g['RecordUtilOracleCharVoList']:
            if c['Label']==lab: return list(map(int,c['Position'].split(',')))
def crops(rn,lab,H=260,p=8):
    x,y,w,h=box(rn,lab); r=d[rn]; cr=(max(0,x-p),max(0,y-p),x+w+p,y+h+p)
    rub=Image.open(OB+'/'+r['Rubbing']).convert('L').crop(cr); fac=Image.open(OB+'/'+r['Facsimile']).convert('L').crop(cr)
    return [up(rub,H),up(ImageOps.invert(ImageOps.autocontrast(rub,cutoff=2)),H),up(fac,H)]
def up(im,H): s=H/im.height; return im.resize((max(1,int(im.width*s)),H),Image.LANCZOS).convert('RGB')
r=d['H30442']
def annot(src):
    im=Image.open(OB+'/'+r[src]).convert('RGB'); D=ImageDraw.Draw(im)
    for g in r['RecordUtilSentenceGroupVoList']:
        for c in g['RecordUtilOracleCharVoList']:
            x,y,w,h=map(int,c['Position'].split(','))
            D.rectangle((x,y,x+w,y+h),outline=(255,0,0) if g['GroupCategory'].endswith('2') else (0,150,255),width=2)
            D.text((x+1,y-1),f"{g['GroupCategory'][-1]}.{c['OrderNumber']}",font=fs,fill=(255,200,0))
    return im.crop((300,20,588,340)).resize((576,640))
rows=[]
rows.append(('① 合30442 OBIMD 框序（2.x＝辞2；2.0/2.1/2.4/2.6/2.9 为版外缺字占位）：2.2卜｜2.3 uw9w7g847l｜2.5 a7al7kr0c5｜2.7王｜2.8賓  ↔ 史语所 30442.2「卜Ｂ４７６Ｔ９王」',[annot('Rubbing'),annot('Facsimile')]))
rows.append(('② 2.3 uw9w7g847l（拓/反相/摹）＝Ｂ４７６位置　对 小学堂附录3775（标合30442）',crops('H30442','uw9w7g847l')+[up(Image.open('/workspace/oracle-bone/raw/xxtapp/3775_0.png').convert('L'),260)]))
rows.append(('③ 2.5 a7al（合30442，Ｔ９位置）拓/反相/摹　→ 右：T9 清晰拓片 合14660 / 14666 / 14679 / 1508',crops('H30442','a7al7kr0c5')+[crops(n,'gaf7rmekoj')[0] for n in ['H14660','H14666','H14679','H1508']]))
rows.append(('④ 合4479 a7al（Ｇ２８２「壬辰卜惟Ｇ２８２令」）拓/反相/摹　→ 右：T9 摹本 合1508 / 32675 / 14673 / 14666',crops('H4479','a7al7kr0c5')+[crops('H1508','gaf7rmekoj')[2],crops('H32675','gaf7rmekoj')[2],crops('H14673','gaf7rmekoj')[2],crops('H14666','gaf7rmekoj')[2]]))
W=max(1400,max(sum(i.width+10 for i in ims) for _,ims in rows)+20)
Ht=60+sum(max(i.height for i in ims)+50 for _,ims in rows)+40
out=Image.new('RGB',(W,Ht),'white'); D=ImageDraw.Draw(out)
D.text((10,10),'合30442 框位复核与合4479 单独复核（OBIMD 拓片/摹本，原图低分辨率放大）【未核：目验】',font=f,fill=0)
y=60
for cap,ims in rows:
    D.text((10,y),cap,font=fs,fill=0); x=10
    for i in ims: out.paste(i,(x,y+24)); x+=i.width+10
    y+=max(i.height for i in ims)+50
D.text((10,y),'合34275（史语所「于Ｔ９父燎雨」）：OBIMD / HUST / 小学堂 均未收，无法切图。',font=fs,fill=(180,0,0))
out.save('/workspace/obc/h30442_recheck.png'); print(out.size)
