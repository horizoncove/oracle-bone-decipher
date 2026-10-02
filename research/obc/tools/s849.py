import sys,glob,os,re;sys.path.insert(0,'/workspace/obc/tools')
from sheetlib import *
def hc(i,n=10,off=0):
    base=resolve_hust_dir(i)
    if not base: return []
    fs=sorted(glob.glob(f'{base}/G_*'))
    fs+=sorted(f for f in glob.glob(f'{base}/*') if os.path.isfile(f) and not os.path.basename(f).startswith('G_'))
    out=[]
    for f in fs[off:off+n]:
        b=os.path.basename(f); m=re.search(r'合(\d+)',b)
        out.append((Image.open(f).convert('L'),('合'+m.group(1)) if m else b.split('_')[0][:10]))
    return out
def xx(cid):
    X=sorted(glob.glob(f'/workspace/obc/data/HUST-OBC/undeciphered/X/{cid}/*'))
    return [(Image.open(f).convert('L'),'附'+os.path.basename(f).split('_')[2]+'-'+os.path.basename(f).split('_')[3].split('.')[0]) for f in X]
rows=[
('X/849 (附7812-14)',xx('849')),
('祀 HUST 1163',hc('1163',14)),
('示 1162',hc('1162',10)),
('卩 0284',hc('0284',10)),
('巳 0609',hc('0609',10)),
('祼 1180',hc('1180',8)),
('祝 1174',hc('1174',8)),
('祐 1170',hc('1170',6)),
('祏 1169',hc('1169',6)),
('戠 0714',hc('0714',6)),
('主 0101',hc('0101',6)),
]
rows=[(a,b) for a,b in rows if b]
for a,b in rows: print(a,len(b))
build(rows,'/workspace/obc/x849_sheet.png',
      title='X/849（附錄7812–7814，k≈660，9例）與祀/示/卩/巳比較　【未核：AI選樣】')
