import sys,glob,os,re;sys.path.insert(0,'/workspace/obc/tools')
from sheetlib import *
B='/tmp/obcj/HUST-OBC/deciphered'; XR='/workspace/oracle-bone/raw/xxtapp/'
L=lambda f:Image.open(f).convert('L')
num=lambda f:int(f.split('_H')[1].split('_')[0])
T9f=sorted(glob.glob('/tmp/t9/gaf7_*_f.png'),key=num)
inr=[f for f in T9f if 14650<=num(f)<=14680]; outr=[f for f in T9f if not 14650<=num(f)<=14680]
X=sorted(glob.glob('/workspace/obc/data/HUST-OBC/undeciphered/X/276/*'))
xa=[(L(f),os.path.basename(f)[4:10]+('光误入' if '_7252_' in f else '')) for f in X]
hp=lambda c,n=None: [(L(f),(re.search(r'合\d+',f).group(0) if re.search(r'合\d+',f) else os.path.basename(f)[:10])) for f in sorted(glob.glob(f'{B}/{c}/G_*'))[:n]]
same=[(f'{B}/1029_1030/1029/G_1029_福18合14660.png','燎 合14660'),(f'{B}/0843/G_0843_前1.49.1合14658.png','東 合14658'),(f'{B}/1397/G_1397_林1.23.13合14680.png','西 合14680'),
 (f'{B}/0040/G_0040_福23合14667.png','㱿 合14667'),(f'{B}/0300/G_0300_拾2.12合34271.png','叀 合34271'),(f'{B}/0949/G_0949_後1.22.3合33273歷組.png','河 合33273'),
 (f'{B}/0318/G_0318_乙5272合1140賓組.png','召 合1140'),(f'{B}/0192/G_0192_粹67合14681賓組.png','兒 合14681'),(f'{B}/1696/G_1696_前1.50.1合10139.png','𠦪 合10139')]
same=[(L(f) if os.path.exists(f) else L(glob.glob(f.replace('/1029_1030/1029/','/*/*/').replace(B+'/',B+'/*/'))[0]),c) for f,c in same if os.path.exists(f) or glob.glob(f)]
rows=[('X/276 (7249–7252)',xa),
('T9=OBIMD gaf7rmekoj(兇) 摹 合14650–14680',[(L(f),'合%d'%num(f)) for f in inr]),
('T9 同上 拓片',[(L(f.replace('_f.png','_r.png')),'合%d'%num(f)) for f in inr]),
('T9 其他版 摹(OBIMD)',[(L(f),'合%d'%num(f)) for f in outr]),
('甲骨文编附录4418(小学堂)',[(L(XR+f'4418_{k}.png'),'4418') for k in range(12) if os.path.exists(XR+f'4418_{k}.png')]),
('OBIMD a7al(Ｇ２８２) 合4479/30442 摹/拓',[(L(f),f.split('_')[1].replace('H','合')+('摹' if f.endswith('_f.png') else '拓')) for f in sorted(glob.glob('/tmp/t9/a7al*'))]),
('附录3775(合30442,旧G282依据)',[(L(XR+'3775_0.png'),'3775')]),
('HUST已释:T9诸版上的他字(非T9)',same),
('光 0187 (最近已释类)',hp('0187',20)),
('夒 0419',hp('0419',24)),
('岳 0597',hp('0597_0598/0597',24)),
('HUST 0185 兇(仅3图,L_)',[(L(f),os.path.basename(f)) for f in sorted(glob.glob(B+'/0185/*'))]),
]
build(rows,'/workspace/obc/x276_vs_t9.png',S=88,cols=16,LW=230,title='X/276 与 T9（OBIMD 兇 gaf7rmekoj）、光、夒、岳、G282/3775 对照　【未核：AI选样/目验】')
