# Embed all undeciphered X images with HUST-OBS MoCo ResNet18; score vs deciphered classes (gallery_12) -> class-to-class matrix
import os,sys,json,collections,torch,torch.nn as nn,torch.nn.functional as F
sys.path.insert(0,'/workspace/obc'); os.chdir('/workspace/obc')
from functools import partial
from torchvision.models import resnet
from torchvision import transforms
from PIL import Image
torch.set_num_threads(6)
R='data/HUST-OBC'; U=R+'/undeciphered/X'; D=R+'/deciphered'
tm=transforms.Compose([transforms.Resize((128,128)),transforms.ToTensor(),transforms.Normalize([0.7482745,0.7510818,0.7501316],[0.36487347,0.36375728,0.36417565])])
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
def embed(paths,bs=128):
    out=[]
    for i in range(0,len(paths),bs):
        out.append(F.normalize(enc(torch.stack([tm(Image.open(p).convert('RGB')) for p in paths[i:i+bs]])),dim=1))
    return torch.cat(out)
qp,ql=[],[]
for c in sorted(os.listdir(U)):
    for f in sorted(os.listdir(f'{U}/{c}')): qp.append(f'{U}/{c}/{f}'); ql.append(c)
Q=embed(qp); print('Q',Q.shape,flush=True)
gp,gl,G=torch.load('gallery_12.pt')
torch.save((qp,ql,Q,gp,gl,G),'/workspace/oracle-bone/screen/emb.pt'); print('saved')
