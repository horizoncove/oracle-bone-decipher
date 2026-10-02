import json,re,html,os,subprocess,io
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
B='https://xiaoxue.iis.sinica.edu.tw'; O='raw/xxtapp'; os.makedirs(O,exist_ok=True)
d=json.load(open('raw/xxt_index.json'))
jobs=[]
for e in d:
    if e['idx'].get('新甲骨文編'): continue
    z=e['zi']; h=open(f'raw/xxtzi_{z}.html',encoding='utf-8',errors='ignore').read()
    items=re.findall(r'class="VariantList[AB]"><img src="([^"]*)"[^>]*/><br />([^<]*)<br />([^<]*)<br />((?:<img[^>]*/>)?[^<]*)<td>',h)
    for k,(s,a,b,c) in enumerate(items):
        jobs.append(dict(zi=z,k=k,src=html.unescape(s).replace('size=36','size=72'),old=a,heji=b,cat=re.sub(r'<img[^>]*/>','𠂤',c),f=f'{O}/{z}_{k}.png'))
json.dump(jobs,open(O+'/meta.json','w'),ensure_ascii=False)
def get(j):
    if os.path.exists(j['f']): return 1
    png=subprocess.run(["curl","-sL","-m","30","-A","Mozilla/5.0",B+j['src']],capture_output=True).stdout
    try:
        im0=Image.open(io.BytesIO(png)).convert('RGBA'); im=Image.new('RGB',im0.size,'white'); im.paste(im0,mask=im0.split()[3]); im.save(j['f']); return 1
    except Exception: return 0
with ThreadPoolExecutor(6) as ex: r=list(ex.map(get,jobs))
print('done',len(jobs),sum(r))
