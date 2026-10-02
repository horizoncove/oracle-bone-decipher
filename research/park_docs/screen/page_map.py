# Map HUST X 正编 undeciphered classes (serial<=6760) to 小学堂(甲骨文编) 字头 via 新甲骨文编 頁.行 index.
import json,os,csv,bisect,collections
r=json.load(open('raw/xxt_index.json')); pts=json.load(open('screen/page_flow.json'))
# anchors: (serial, page) ; keep longest increasing subsequence in page when sorted by serial
a=sorted(set((p[1],p[0]) for p in pts))
# LIS on page
import numpy as np
n=len(a); best=[1]*n; prev=[-1]*n
for i in range(n):
    for j in range(max(0,i-60),i):
        if a[j][1]<=a[i][1] and a[j][0]<a[i][0] and best[j]+1>best[i]: best[i]=best[j]+1; prev[i]=j
i=int(np.argmax(best)); lis=[]
while i>=0: lis.append(a[i]); i=prev[i]
lis=lis[::-1]; S=np.array([x[0] for x in lis],float); P=np.array([x[1] for x in lis],float)
print('anchors',len(a),'LIS',len(lis))
U='/workspace/obc/data/HUST-OBC/undeciphered/X'
pages=[]
for x in r:
    for pg in x['idx'].get('新甲骨文編','').split('、'):
        try: pages.append((float(pg),x))
        except: pass
pages.sort(key=lambda t:t[0]); pk=[t[0] for t in pages]
rows=[]
for c in os.listdir(U):
    ser=[int(f.split('_')[2]) for f in os.listdir(f'{U}/{c}')]; s0,s1=min(ser),max(ser)
    if s0>6760: continue
    # bracketing anchors
    k0=bisect.bisect_right(S,s0)-1; k1=bisect.bisect_left(S,s1)
    if k0<0 or k1>=len(S): continue
    lo,hi=P[k0],P[k1]
    cand=[(pg,x) for pg,x in pages[bisect.bisect_left(pk,lo):bisect.bisect_right(pk,hi)]]
    # exclude 字头 that are themselves anchors (already HUST-deciphered with X files)
    anchor_zi=set(p[3] for p in pts)
    cand=[(pg,x) for pg,x in cand if x['zi'] not in anchor_zi]
    est=float(np.interp((s0+s1)/2,S,P))
    cand.sort(key=lambda t:abs(t[0]-est))
    cats=lambda x:';'.join(f'{k}{v}' for k,v in collections.Counter(i[2] or '無' for i in x['items']).items())
    rows.append([f'X/{c}',s0,s1,len(ser),f'{lo:.1f}-{hi:.1f}',f'{est:.1f}',len(cand)]+sum([[x['zi'],x['kai'],x['n'],pg,cats(x),' '.join(i[1] for i in x['items'][:8] if i[1])] for pg,x in cand[:3]],[]))
rows.sort(key=lambda t:t[1])
hdr=['x_class','serial_min','serial_max','n_img','新page_window','新page_est','n_xxt_candidates']
for k in (1,2,3): hdr+= [f'xxt{k}_zi',f'xxt{k}_kai',f'xxt{k}_n',f'xxt{k}_新page',f'xxt{k}_類組',f'xxt{k}_合集(前8)']
with open('03-screen-X正编未释_vs_小学堂字头.csv','w',newline='') as f: w=csv.writer(f); w.writerow(hdr); w.writerows(rows)
c=collections.Counter(min(t[6],3) for t in rows); print('X 正编 classes mapped',len(rows),'by #candidates (3=3+)',dict(c))
uniq=[t for t in rows if t[6]==1]; print('unique-candidate classes',len(uniq))
for t in rows:
    if t[0] in ('X/1370','X/1366','X/1850','X/2230','X/2213','X/1401','X/2190','X/1814','X/2109','X/2173'): print(t[:13])
