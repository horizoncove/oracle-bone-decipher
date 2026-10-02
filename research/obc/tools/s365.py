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
X=sorted(glob.glob('/workspace/obc/data/HUST-OBC/undeciphered/X/365/*'))
xa=[(Image.open(f).convert('L'),'附'+os.path.basename(f).split('_')[2]+'-'+os.path.basename(f).split('_')[3][0]) for f in X]
obmei=[(i,n+'摹') for i,n in obimd('fbmole6hwm',5)]+[(i,n+'拓') for i,n in obimd('fbmole6hwm',4,src='rubbing')]
obmei2=[(i,n+'摹') for i,n in obimd('mxjh9h64im',5)]+[(i,n+'拓') for i,n in obimd('mxjh9h64im',4,src='rubbing')]
cuhk=[]
for f in sorted(glob.glob('/workspace/obc/gx/mei_7709*.jpg')):
    cuhk.append((Image.open(f).convert('L'),'CUHK眉'))
rows=[
('X/365 (附7349-50)',xa),
('眉 HUST 1145',hc('1145',14)),
('眉 OBIMD',obmei),
('眉 CUHK甲骨',cuhk),
('湄 HUST 0979',hc('0979',12)),
('湄 OBIMD',obmei2),
('目 1139',hc('1139',10)),
('省 1144',hc('1144',10)),
('舌 1322 (袁0243弱)',hc('1322',8)),
('山 0595',hc('0595',6)),
]
rows=[r for r in rows if r[1]]
build(rows,sys.argv[1] if len(sys.argv)>1 else '/workspace/obc/x365_sheet.png',
      title='X/365（附錄7349–7350，k≈224，8例）與眉/湄/目/省比較　【未核：AI選樣】')
