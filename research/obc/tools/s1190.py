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
X=sorted(glob.glob('/workspace/obc/data/HUST-OBC/undeciphered/X/1190/*'))
xa=[(Image.open(f).convert('L'),'附'+os.path.basename(f).split('_')[2]+'-'+os.path.basename(f).split('_')[3][0]) for f in X]
# OBIMD unencoded on H6980 (Lian A1)
ob6980=[(i,'H6980摹') for i,_ in obimd('hruffydq1k',2,names=['H6980'])]+[(i,'H6980拓') for i,_ in obimd('hruffydq1k',2,src='rubbing',names=['H6980'])]
# OBIMD 璞 (standard)
obpu=[(i,n+'摹') for i,n in obimd('gcbnox9x1n',4)]+[(i,n+'拓') for i,n in obimd('gcbnox9x1n',4,src='rubbing')]
# CUHK 僕
cuhk=[]
for f in sorted(glob.glob('/workspace/obc/gx/pu2_*.jpg')):
    cuhk.append((Image.open(f).convert('L'),'CUHK僕'))
rows=[
('X/1190 (附8144-45)',xa),
('OBIMD H6980 未编码',ob6980),
('璞 HUST 1075',hc('1075',12)),
('璞 OBIMD H6817等',obpu),
('僕 HUST 0177',hc('0177',8)),
('僕 CUHK甲骨',cuhk),
('弄 0642',hc('0642',8)),
('玉 1069',hc('1069',8)),
('對 0575',hc('0575',8)),
('買 1444',hc('1444',6)),
('周 0348',hc('0348',6)),
]
rows=[r for r in rows if r[1]]
build(rows,sys.argv[1] if len(sys.argv)>1 else '/workspace/obc/x1190_sheet.png',
      title='X/1190（附錄8144–8145，k≈968，8例）與璞/僕/弄比較　【未核：AI選樣】')
