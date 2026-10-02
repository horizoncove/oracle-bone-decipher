# X/276 vs T9 (OBIMD gaf7rmekoj=兇) embedding comparison
import os,sys,glob,json,collections,torch,torch.nn as nn,torch.nn.functional as F,torchvision
sys.path.insert(0,'/workspace/obc'); os.chdir('/workspace/obc')
from torchvision import transforms
from torchvision.models import resnet
from functools import partial
from PIL import Image
torch.set_num_threads(8)
D='data/HUST-OBC/deciphered'; id2ch=json.load(open(D+'/ID_to_chinese.json'))
tm=transforms.Compose([transforms.Resize((128,128)),transforms.ToTensor(),transforms.Normalize([0.7482745,0.7510818,0.7501316],[0.36487347,0.36375728,0.36417565])])
tv=transforms.Compose([transforms.Resize((128,128)),transforms.ToTensor(),transforms.Normalize([0.85233593,0.85246795,0.8517555],[0.31232414,0.3122127,0.31273854])])
def pad_sq(im):
    w,h=im.size; m=max(w,h); n=Image.new('RGB',(m,m),(255,255,255)); n.paste(im,((m-w)//2,(m-h)//2)); return n
class SBN(nn.BatchNorm2d):
    def __init__(s,f,num_splits,**kw): super().__init__(f,**kw)
def base(dim=128,arch='resnet18'):
    n=getattr(resnet,arch)(num_classes=dim,norm_layer=partial(SBN,num_splits=8)); L=[]
    for name,m in n.named_children():
        if name=='conv1': m=nn.Conv2d(3,64,3,1,1,bias=False)
        if isinstance(m,nn.MaxPool2d): continue
        if isinstance(m,nn.Linear): L.append(nn.Flatten(1))
        L.append(m)
    return nn.Sequential(*L)
enc=base(); sd=torch.load('weights/moco_model_last.pth',map_location='cpu',weights_only=False)['state_dict']
enc.load_state_dict({k[len('encoder_q.net.'):]:v for k,v in sd.items() if k.startswith('encoder_q.net.')}); enc.eval()
@torch.no_grad()
def emb(ps): return F.normalize(enc(torch.stack([tm(Image.open(p).convert('RGB')) for p in ps])),dim=1)
vl=json.load(open('HUST-OBS/Validation/Validation_label.json')); idx2key={v:k for k,v in vl.items()}
net=torchvision.models.resnet50(); net.fc=nn.Linear(net.fc.in_features,1588)
net.load_state_dict(torch.load('weights/val_max_val_acc.pth',map_location='cpu',weights_only=False)['state_dict']); net.eval()
def k2c(k): return '/'.join(dict.fromkeys(id2ch.get(i,'?') for i in k.split('_')))
X=sorted(f for f in glob.glob('data/HUST-OBC/undeciphered/X/276/*') if '_7252_' not in f)
X52=sorted(glob.glob('data/HUST-OBC/undeciphered/X/276/*_7252_*'))
T9f=sorted(glob.glob('/tmp/t9/gaf7_*_f.png')); T9r=sorted(glob.glob('/tmp/t9/gaf7_*_r.png'))
A7f=sorted(glob.glob('/tmp/t9/a7al_*_f.png'))
xm=json.load(open('/workspace/oracle-bone/raw/xxtapp/meta.json'))
Z=lambda z:['/workspace/oracle-bone/'+j['f'] for j in xm if str(j['zi'])==str(z)]
H185=sorted(glob.glob(D+'/0185/*'))
sets=dict(X276=X,X7252=X52,T9_fac=T9f,T9_rub=T9r,a7al_fac=A7f,xxt4418=Z(4418),xxt3775=Z(3775),hust0185_兇=H185,
  hust0187_光=sorted(glob.glob(D+'/0187/*'))[:40],hust0419_夒=sorted(glob.glob('/tmp/obcj/HUST-OBC/deciphered/0419/G_*')),hust0597_岳=sorted(glob.glob('/tmp/obcj/HUST-OBC/deciphered/0597_0598/059?/G_*')),hust0187光G=sorted(glob.glob(D+'/0187/G_*')))
E={k:emb(v) for k,v in sets.items() if v}
def mm(a,b):  # mean over a of max over b
    S=E[a]@E[b].T
    if a==b: S=S-2*torch.eye(len(S))
    return round(float(S.max(1).values.mean()),3)
print('n:',{k:len(v) for k,v in sets.items()})
keys=list(E)
print('mean-of-max sim (row=query):'); print('%-14s'%''+' '.join('%9s'%k[:9] for k in keys))
for a in keys: print('%-14s'%a+' '.join('%9.3f'%mm(a,b) for b in keys))
# OBIMD calibration: rank T9 & a7al among OBIMD crop gallery labels (G.pt, 417 mostly-unencoded labels)
cm=json.load(open('/workspace/oracle-bone/obimd/crops_meta.json')); G=torch.load('/workspace/oracle-bone/obimd/G.pt')
labs=[c['label'] or 'None' for c in cm]+['gaf7rmekoj(T9)']*len(T9f)+['a7al7kr0c5']*len(A7f)
GG=torch.cat([G,E['T9_fac'],E['a7al_fac']])
ul=sorted(set(labs)); li={l:i for i,l in enumerate(ul)}; ix=torch.tensor([li[l] for l in labs])
S=E['X276']@GG.T; M=torch.full((len(S),len(ul)),-1.0).scatter_reduce(1,ix.expand(len(S),-1),S,reduce='amax').mean(0)
t=M.topk(8); print('X276 vs OBIMD crop labels top8:',[(ul[i],round(float(v),3)) for v,i in zip(t.values,t.indices)])
# HUST deciphered gallery
gp,gl,GH=torch.load('gallery_12.pt',weights_only=False)
ulh=sorted(set(gl)); lih={l:i for i,l in enumerate(ulh)}; ixh=torch.tensor([lih[l] for l in gl])
for q in ['X276','T9_fac','T9_rub','a7al_fac']:
    S=E[q]@GH.T; M=torch.full((len(S),len(ulh)),-1.0).scatter_reduce(1,ixh.expand(len(S),-1),S,reduce='amax').mean(0)
    t=M.topk(6); print(q,'vs HUST deciphered (MoCo) top6:',[(ulh[i],id2ch.get(ulh[i].split('_')[0],'?'),round(float(v),3)) for v,i in zip(t.values,t.indices)])
for q in ['X276','T9_fac','T9_rub']:
    with torch.no_grad(): P=F.softmax(net(torch.stack([tv(pad_sq(Image.open(p).convert('RGB'))) for p in sets[q]])),1)
    mp=P.mean(0); t=mp.topk(5); votes=collections.Counter(int(i) for i in P.argmax(1))
    print(q,'ResNet50 top5:',[(k2c(idx2key[int(i)]),idx2key[int(i)],round(float(v),3),votes.get(int(i),0)) for v,i in zip(t.values,t.indices)])
# per-T9 crop nearest X276 sim
S=E['T9_fac']@E['X276'].T
print('per T9 fac crop max sim to X276:',[(os.path.basename(p).split('_')[1],round(float(v),2)) for p,v in zip(T9f,S.max(1).values)])
S=E['a7al_fac']@E['X276'].T; print('a7al per crop:',[(os.path.basename(p).split('_')[1],round(float(v),2)) for p,v in zip(A7f,S.max(1).values)])
