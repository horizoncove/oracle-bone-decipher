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
# also try OBIMD
rows=[
('X/956 (附7917-21)',xx('956')),
('丙 HUST 0093',hc('0093',14)),
('商 0358',hc('0358',12)),
('尚 0579',hc('0579',10)),
('高 1614',hc('1614',10)),
('貞 1438',hc('1438',8)),
('斝 0758',hc('0758',8)),
('晶 0795',hc('0795',6)),
('几 0224',hc('0224',6)),
]
rows=[(a,b) for a,b in rows if b]
for a,b in rows: print(a,len(b))
build(rows,'/workspace/obc/x956_sheet.png',
      title='X/956（附錄7917–7921，k≈757，18例）與丙/商/尚/高比較　【未核：AI選樣】')
