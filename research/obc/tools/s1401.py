import sys,glob,os,re;sys.path.insert(0,'/workspace/obc/tools')
from sheetlib import *
def hc(i,n=10,off=0):
    fs=sorted(glob.glob(f'{HD}/{i}/G_*'))
    fs+=sorted(f for f in glob.glob(f'{HD}/{i}/*') if not os.path.basename(f).startswith('G_'))
    out=[]
    for f in fs[off:off+n]:
        b=os.path.basename(f); m=re.search(r'合(\d+)',b)
        out.append((Image.open(f).convert('L'),('合'+m.group(1)) if m else b.split('_')[0]))
    return out
X=sorted(glob.glob('/workspace/obc/data/HUST-OBC/undeciphered/X/1401/*'))
xa=[(Image.open(f).convert('L'),'#'+os.path.basename(f).split('_')[2]+'-'+os.path.basename(f).split('_')[3][0]) for f in X]
ob=[(i,n+'摹') for i,n in obimd('04jjwtizii',3)]+[(i,n+'拓') for i,n in obimd('04jjwtizii',3,src='rubbing')]
rows=[('X/1401 (#2040-46)',xa),('OBIMD 合1439/3914/18204',ob),
('叀 0300',hc('0300',24)),
('叀 (OBIMD)',obimd('7grlc2aopw',12)),
('專 0571',hc('0571',12)),
('東 0843',hc('0843',8)),
('克 0188',hc('0188',8)),
('幼 0623',hc('0623',8)),
('幽 0624',hc('0624',8)),


('永 0926 (賓組貞人)',hc('0926',12)),('入/內 (OBIMD 入)',obimd('a8n7ywfrd3',10)),('索 1226',hc('1226',12)),('系 1223',hc('1223',8)),('糸 1222',hc('1222',6)),('轡 1458',hc('1458',8)),('率 1068',hc('1068',6)),('奚 0442',hc('0442',6)),
]
rows=[r for r in rows if r[1]]
build(rows,sys.argv[1] if len(sys.argv)>1 else '/workspace/obc/x1401_sheet.png',title='X/1401（#2040–2046，27例）與叀/專/東/克/糸系/索字比較（本地無𤔔圖）【未核：AI選樣】')
