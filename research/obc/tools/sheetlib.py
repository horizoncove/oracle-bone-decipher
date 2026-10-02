import json,glob,os,subprocess
from PIL import Image, ImageDraw, ImageFont
FONT='/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
HD='/workspace/obc/data/HUST-OBC/deciphered'
OB='/workspace/obimd'
_d=None;_m=None
def resolve_hust_dir(i):
    i=str(i)
    direct=f'{HD}/{i}'
    if os.path.isdir(direct) and any(os.path.isfile(os.path.join(direct,f)) for f in os.listdir(direct)):
        return direct
    # nested under combined folders e.g. 1290_1291_1292/1290, 1163_1164/1163
    for c in sorted(glob.glob(f'{HD}/{i}_*')+glob.glob(f'{HD}/*_{i}')+glob.glob(f'{HD}/*_{i}_*')):
        if os.path.isdir(os.path.join(c,i)): return os.path.join(c,i)
        if os.path.isdir(c) and any(os.path.isfile(os.path.join(c,f)) for f in os.listdir(c)):
            return c
    sub=glob.glob(f'{HD}/*/{i}')
    for s in sub:
        if os.path.isdir(s): return s
    return None
def hust(i,n=10,prefer='G_'):
    base=resolve_hust_dir(i)
    if not base: return []
    fs=sorted(glob.glob(f'{base}/*'))
    fs=[f for f in fs if os.path.isfile(f)]
    g=[f for f in fs if os.path.basename(f).startswith(prefer)]
    o=[f for f in fs if f not in g]
    return [Image.open(f).convert('L') for f in (g+o)[:n]]
def files(fs): return [Image.open(f).convert('L') for f in fs]
def obimd(label,n=10,src='facsimile',names=None,pad=4):
    global _d
    if _d is None: _d=json.load(open(f'{OB}/data.json'))
    out=[]
    for r in _d:
        if names and r['RubbingName'] not in names: continue
        for g in r['RecordUtilSentenceGroupVoList']:
            for c in g['RecordUtilOracleCharVoList']:
                if c['Label']==label:
                    x,y,w,h=map(int,c['Position'].split(','))
                    p=f"{OB}/{src}/{os.path.basename(r[src.capitalize()])}"
                    if not os.path.exists(p):
                        subprocess.run(['unzip','-o','-q',f'{OB}/rubbing.zip',f'rubbing/{os.path.basename(p)}','-d',OB])
                    im=Image.open(p).convert('L').crop((max(0,x-pad),max(0,y-pad),x+w+pad,y+h+pad))
                    out.append((im,r['RubbingName']))
                    if len(out)>=n: return out
    return out
def fit(im,S):
    im=im.copy(); im.thumbnail((S-6,S-6)); c=Image.new('L',(S,S),255)
    c.paste(im,((S-im.width)//2,(S-im.height)//2)); return c
def build(rows,out,S=96,cols=12,title=None,LW=170):
    f=ImageFont.truetype(FONT,22); fs=ImageFont.truetype(FONT,13)
    H=(50 if title else 10)
    for lab,ims in rows: H+=((max(1,len(ims))+cols-1)//cols)*(S+16)+6
    img=Image.new('L',(LW+cols*S,H),255);d=ImageDraw.Draw(img);y=10
    if title: d.text((10,8),title,font=f,fill=0);y=50
    for lab,ims in rows:
        d.line((0,y-3,img.width,y-3),fill=180)
        d.text((6,y+4),lab,font=f if len(lab)<8 else fs,fill=0)
        for k,it in enumerate(ims):
            im,cap=it if isinstance(it,tuple) else (it,'')
            X=LW+(k%cols)*S;Y=y+(k//cols)*(S+16)
            img.paste(fit(im,S),(X,Y)); d.text((X+2,Y+S),cap[:14],font=fs,fill=60)
        y+=((max(1,len(ims))+cols-1)//cols)*(S+16)+6
    img.save(out);print(out,img.size)
