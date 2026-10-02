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
('X/462 (附7444-46)',xx('462')),
('X/461 (附7440-43 同族)',xx('461')[:10]),
('肇 HUST 1290',hc('1290',12)),
('肈 1291',hc('1291',8)),
('肁 1292',hc('1292',4)),
('啟 0362',hc('0362',10)),
('啓 0363',hc('0363',8)),
('启 0342',hc('0342',8)),
('戶 0718',hc('0718',10)),
('户 0719',hc('0719',8)),
('攴 0741',hc('0741',8)),
('取 0310',hc('0310',8)),
('畋 1093',hc('1093',8)),
]
rows=[(a,b) for a,b in rows if b]
for a,b in rows: print(a,len(b))
build(rows,'/workspace/obc/x462_sheet.png',
      title='X/462（附錄7444–7446，k≈311，10例）與肇/啟/戶/攴比較　【未核：AI選樣】')
