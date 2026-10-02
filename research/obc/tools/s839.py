import sys,glob,os,re;sys.path.insert(0,'/workspace/obc/tools')
from sheetlib import *
def hc(i,n=10,off=0):
    fs=sorted(glob.glob(f'{HD}/{i}/G_*'))
    fs+=sorted(f for f in glob.glob(f'{HD}/{i}/*') if not os.path.basename(f).startswith('G_'))
    out=[]
    for f in fs[off:off+n]:
        b=os.path.basename(f); m=re.search(r'合(\d+)',b)
        out.append((Image.open(f).convert('L'),('合'+m.group(1)) if m else b.split('_')[0][:10]))
    return out
X=sorted(glob.glob('/workspace/obc/data/HUST-OBC/undeciphered/X/839/*'))
xa=[(Image.open(f).convert('L'),'附'+os.path.basename(f).split('_')[2]+'-'+os.path.basename(f).split('_')[3][0]) for f in X]
obyan=[(i,n+'摹') for i,n in obimd('xl187q597e',8)]+[(i,n+'拓') for i,n in obimd('xl187q597e',6,src='rubbing')]
rows=[
('X/839 (附7801-03)',xa),
('燕 HUST 1031',hc('1031',16)),
('燕 OBIMD',obyan),
('隹 1544',hc('1544',10)),
('雀 1547',hc('1547',10)),
('鳥 1634',hc('1634',8)),
('鷄 1642',hc('1642',6)),
('魚 1629',hc('1629',6)),
('美 1253',hc('1253',6)),
]
rows=[r for r in rows if r[1]]
build(rows,sys.argv[1] if len(sys.argv)>1 else '/workspace/obc/x839_sheet.png',
      title='X/839（附錄7801–7803，k≈651，9例）與燕/隹/雀/鳥比較　【未核：AI選樣】')
