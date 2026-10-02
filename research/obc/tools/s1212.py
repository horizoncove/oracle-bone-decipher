import sys,glob,os,re;sys.path.insert(0,'/workspace/obc/tools')
from sheetlib import *
X=sorted(glob.glob('/workspace/obc/data/HUST-OBC/undeciphered/X/1212/*'))
xa=[(Image.open(f).convert('L'),'#'+os.path.basename(f).split('_')[2]+'-'+os.path.basename(f).split('_')[3][0]) for f in X]
A=sorted(f for f in glob.glob('/workspace/obc/data/HUST-OBC/undeciphered/X/276/*') if '7252' not in f)[:6]
rows=[('X/1212 (#8167-71)',xa),
('OBIMD T54 摹',[(i,n) for i,n in obimd('jyskjcj861',12)]),
('OBIMD T54 拓',[(i,n) for i,n in obimd('jyskjcj861',12,src='rubbing')]),
('X/276 (參照)',files(A))]
build(rows,'/workspace/obc/x1212_sheet.png',title='X/1212（附錄 #8167–8171，20例）與 OBIMD 同字頭 jyskjcj861、X/276 對照【未核】')
