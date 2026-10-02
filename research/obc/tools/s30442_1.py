import json,random
from PIL import Image,ImageDraw,ImageFont,ImageOps
OB='/workspace/obimd'; FONT='/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
D_=json.load(open(OB+'/data.json')); d={r['RubbingName']:r for r in D_}
f=ImageFont.truetype(FONT,22); fs=ImageFont.truetype(FONT,15)
def up(im,H): s=H/im.height; return im.resize((max(1,int(im.width*s)),H),Image.LANCZOS).convert('RGB')
def crop(r,pos,src,p=8):
    x,y,w,h=map(int,pos.split(',')); im=Image.open(OB+'/'+r[src]).convert('L')
    return im.crop((max(0,x-p),max(0,y-p),x+w+p,y+h+p))
r=d['H30442']
g1=[g for g in r['RecordUtilSentenceGroupVoList'] if g['GroupCategory']=='InscriptionSentence1'][0]
cs=sorted(g1['RecordUtilOracleCharVoList'],key=lambda c:c['OrderNumber'])
print([(c['OrderNumber'],c['Label'],c['SubLabel'],c['Position']) for c in cs])
last=cs[-1]
# context: 辞1 region
rub=Image.open(OB+'/rubbing/h30442.jpg').convert('RGB'); fac=Image.open(OB+'/facsimile/h30442.jpg').convert('RGB')
def ann(im):
    im=im.copy(); Dd=ImageDraw.Draw(im)
    for c in cs:
        x,y,w,h=map(int,c['Position'].split(',')); Dd.rectangle((x,y,x+w,y+h),outline=(255,0,0),width=2); Dd.text((x+2,y),f"1.{c['OrderNumber']}",font=fs,fill=(255,200,0))
    return up(im.crop((110,70,300,320)),320)
row1=[ann(rub),ann(fac)]
a=crop(r,last['Position'],'Rubbing'); row2=[up(a,320),up(ImageOps.invert(ImageOps.autocontrast(a,cutoff=2)),320),up(crop(r,last['Position'],'Facsimile'),320)]
def ex(label,n,src='Facsimile'):
    out=[]; random.seed(1); recs=D_[:]; random.shuffle(recs)
    for rr in recs:
        for g in rr['RecordUtilSentenceGroupVoList']:
            for c in g['RecordUtilOracleCharVoList']:
                if c['Label']==label and rr['RubbingName']!='H30442':
                    out.append((up(crop(rr,c['Position'],src,4),130),rr['RubbingName'])); break
            if out and out[-1][1]==rr['RubbingName']: break
        if len(out)>=n: break
    return out
# prefer 無名/何组 era plates near 30442 (H27xxx-31xxx) for 雨/河
def ex2(label,n,lo,hi):
    out=[]
    for rr in D_:
        try: k=int(rr['RubbingName'][1:])
        except: continue
        if not lo<=k<=hi: continue
        for g in rr['RecordUtilSentenceGroupVoList']:
            hit=[c for c in g['RecordUtilOracleCharVoList'] if c['Label']==label]
            if hit: out.append((up(crop(rr,hit[0]['Position'],'Facsimile',4),130),rr['RubbingName'])); break
        if len(out)>=n: break
    return out
rows=[('① 合30442 辞1 框位（拓/摹）',[(i,'') for i in row1]),('② 辞1 末字 1.%d（%s）拓/反相/摹'%(last['OrderNumber'],last['Label']),[(i,'') for i in row2]),
('③ OBIMD 雨 ftj0qy2f7b（合27000–31999 摹）',ex2('ftj0qy2f7b',10,27000,31999)),('④ OBIMD 雨（其他组）',ex('ftj0qy2f7b',8)),
('⑤ OBIMD 河 yfnx5cwgq6（合27000–31999 摹）',ex2('yfnx5cwgq6',10,27000,31999)),('⑥ OBIMD 河（其他组）',ex('yfnx5cwgq6',8))]
W=1400; H=60+sum((max(i.height for i,_ in ims) if ims else 130)+50 for _,ims in rows)
out=Image.new('RGB',(W,H),'white'); Dd=ImageDraw.Draw(out); Dd.text((10,10),'合30442 辞1 末字：河 or 雨？（史语所「其遘河」／OBIMD「其冓雨」）【未核：目验】',font=f,fill=0)
y=60
for cap,ims in rows:
    Dd.text((10,y),cap,font=fs,fill=0); x=10; mh=max(i.height for i,_ in ims) if ims else 130
    for i,c in ims:
        if x+i.width>W: break
        out.paste(i,(x,y+24)); Dd.text((x,y+26+i.height-18),c,font=fs,fill=(200,0,0)); x+=i.width+10
    y+=mh+50
out.save('/workspace/obc/h30442_1_he_yu.png'); print(out.size)
