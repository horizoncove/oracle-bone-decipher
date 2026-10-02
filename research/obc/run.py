import os, json, random, time, collections
import numpy as np, torch, torch.nn as nn, torch.nn.functional as F, torchvision
from torchvision import transforms
from torchvision.models import resnet
from functools import partial
from PIL import Image
torch.set_num_threads(8); torch.manual_seed(0); random.seed(0)
R='data/HUST-OBC'; U=R+'/undeciphered'; D=R+'/deciphered'
id2ch=json.load(open(D+'/ID_to_chinese.json'))
# ---- choose 20 classes: 15 largest X classes + 5 Y+H classes (all Y+H top classes tie at 25 imgs; take first 5 by sorted id)
allc=[]
for s in ['L','X','Y+H']:
    for c in os.listdir(f'{U}/{s}'):
        allc.append((len(os.listdir(f'{U}/{s}/{c}')),s,c))
allc.sort(key=lambda t:(-t[0],t[1],t[2]))
xs=[t for t in allc if t[1]=='X'][:15]
yh=sorted([t for t in allc if t[1]=='Y+H' and t[0]==25],key=lambda t:t[2])[:5]
sel=xs+yh
def files(s,c): return sorted(os.path.join(U,s,c,f) for f in os.listdir(f'{U}/{s}/{c}'))
def load(p):
    im=Image.open(p).convert('RGB'); return im
def pad_sq(im):
    w,h=im.size; m=max(w,h); n=Image.new('RGB',(m,m),(255,255,255)); n.paste(im,((m-w)//2,(m-h)//2)); return n
tv=transforms.Compose([transforms.Resize((128,128)),transforms.ToTensor(),transforms.Normalize([0.85233593,0.85246795,0.8517555],[0.31232414,0.3122127,0.31273854])])
tm=transforms.Compose([transforms.Resize((128,128)),transforms.ToTensor(),transforms.Normalize([0.7482745,0.7510818,0.7501316],[0.36487347,0.36375728,0.36417565])])
# ---- Method A: ResNet50 closed-set classifier (HUST-OBC Validation model, 1588 deciphered classes)
vl=json.load(open('HUST-OBS/Validation/Validation_label.json')); idx2key={v:k for k,v in vl.items()}
def key2ch(k): return '/'.join(dict.fromkeys(id2ch.get(i,'?') for i in k.split('_')))
net=torchvision.models.resnet50(); net.fc=nn.Linear(net.fc.in_features,1588)
net.load_state_dict(torch.load('weights/val_max_val_acc.pth',map_location='cpu',weights_only=False)['state_dict']); net.eval()
# ---- Method B: MoCo ResNet18 embedding kNN against deciphered gallery
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
def embed(paths,bs=64):
    out=[]
    for i in range(0,len(paths),bs):
        x=torch.stack([tm(load(p)) for p in paths[i:i+bs]]); out.append(F.normalize(enc(x),dim=1))
    return torch.cat(out)
GPER=int(os.environ.get('GPER','12'))
gcache=f'gallery_{GPER}.pt'
if os.path.exists(gcache): gp,gl,G=torch.load(gcache)
else:
    gp,gl=[],[]
    bycls=collections.defaultdict(list)
    for root,_,fl in os.walk(D):
        for f in fl:
            if not f.endswith('.json'): bycls[os.path.basename(root)].append(os.path.join(root,f))
    for c in sorted(bycls):
        fs=sorted(bycls[c]); random.Random(c).shuffle(fs)
        for f in fs[:GPER]: gp.append(f); gl.append(c)
    t=time.time(); G=embed(gp); print('gallery',len(gp),'embedded in',round(time.time()-t),'s',flush=True)
    torch.save((gp,gl,G),gcache)
res=[]
for n,s,c in sel:
    fs=files(s,c)
    with torch.no_grad():
        x=torch.stack([tv(pad_sq(load(p))) for p in fs]); P=F.softmax(net(x),1)
    mp=P.mean(0); top=mp.topk(3)
    votes=collections.Counter(int(i) for i in P.argmax(1))
    A=[(key2ch(idx2key[int(i)]),idx2key[int(i)],float(v),votes.get(int(i),0)) for v,i in zip(top.values,top.indices)]
    Q=embed(fs); S=Q@G.T   # n x Ngal cosine
    # per class score: for each query image, max sim to each deciphered class; then mean over query images
    labs=sorted(set(gl)); li={l:j for j,l in enumerate(labs)}; lab_idx=torch.tensor([li[l] for l in gl])
    M=torch.full((S.shape[0],len(labs)),-1.0).scatter_reduce(1,lab_idx.expand(S.shape[0],-1),S,reduce='amax')
    cs=M.mean(0); tb=cs.topk(3)
    nn1=collections.Counter(gl[int(j)] for j in S.argmax(1))
    B=[(id2ch.get(labs[int(i)],'?'),labs[int(i)],float(v),nn1.get(labs[int(i)],0)) for v,i in zip(tb.values,tb.indices)]
    # best-matching gallery image for top-1 MoCo class (for contact sheet)
    j1=[k for k,l in enumerate(gl) if l==labs[int(tb.indices[0])]]
    bestg=gp[j1[int(S[:,j1].mean(0).argmax())]]
    # representative image: query image with highest mean sim to the other images in its class
    rep=fs[int((Q@Q.T).mean(1).argmax())]
    intra=float(((Q@Q.T).sum()-len(fs))/(len(fs)*(len(fs)-1)))
    # a top-1 deciphered sample for classifier result too
    k0=A[0][1]; ga=sorted(os.path.join(r,f) for r,_,fl in os.walk(f'{D}/{k0}') for f in fl)
    res.append(dict(cls=f'{s}/{c}',n=n,rep=rep,intra_sim=intra,A=A,B=B,moco_img=bestg,cls_img=ga[0]))
    print(s,c,n,[(a[0],round(a[2],3),a[3]) for a in A],[(b[0],round(b[2],3),b[3]) for b in B],flush=True)
json.dump(res,open('raw_results.json','w'),ensure_ascii=False,indent=1)
