import sys,glob,os,re;sys.path.insert(0,'/workspace/obc/tools')
from sheetlib import *
def hc(i,n=10):
    fs=sorted(glob.glob(f'{HD}/{i}/G_*'))[:n]
    if len(fs)<n: fs+=sorted(f for f in glob.glob(f'{HD}/{i}/*') if not os.path.basename(f).startswith('G_'))[:n-len(fs)]
    out=[]
    for f in fs:
        b=os.path.basename(f); m=re.search(r'合(\d+)',b)
        out.append((Image.open(f).convert('L'),('合'+m.group(1)) if m else b.split('_')[0]))
    return out
X=sorted(f for f in glob.glob('/workspace/obc/data/HUST-OBC/undeciphered/X/276/*') if re.search(r'_725[01]_|_7249_',f))
xa=[(Image.open(f).convert('L'),'附'+os.path.basename(f).split('_')[2]+'-'+os.path.basename(f).split('_')[3][0]) for f in X]
rows=[('X/276 (附7249-51)',xa),
('OBIMD 合4479/30442',[(i,n+' 摹') for i,n in obimd('a7al7kr0c5',5)]+[(i,n+' 拓') for i,n in obimd('a7al7kr0c5',5,src='rubbing')]),
('光 0187',hc('0187',12)),
('羌 1252',hc('1252',12)),
('美 1253',hc('1253',12)),
('萈 1353',hc('1353',8)),
('茍 (CUHK字庫/OBIMD)',[(Image.open(f'/workspace/obc/gx/gou_830d-{i}.jpg').convert('L'),'CHANT'+c) for i,c in [('1335949938','0328'),('1335949969','0328A'),('1335949995','0330B')]]+[(i,n) for i,n in obimd('z6mdb6y8rn',1)]),
('羊 1250',hc('1250',8)),
('若 (OBIMD)',obimd('1k9ogi7w79',12)),
('兄 0183',hc('0183',8)),
('祝 1174',hc('1174',8)),
('鬼 1627',hc('1627',6)),
('異 1100',hc('1100',6)),
('熯 1026',hc('1026',6)),
('堇 0405',hc('0405',6)),
]
build(rows,sys.argv[1] if len(sys.argv)>1 else '/workspace/obc/x276b_sheet.png',title='X/276（附錄7249–7251，12例）與頭頂有附件之人形字比較　【未核：AI選樣】')
