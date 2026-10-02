import subprocess,os,sys
from concurrent.futures import ThreadPoolExecutor
B='https://xiaoxue.iis.sinica.edu.tw/jiaguwen/PageResult/PageResult'
def g(z):
    p=f'raw/xxtzi_{z}.html'
    if os.path.exists(p) and os.path.getsize(p)>2000: return
    h=subprocess.run(["curl","-sL","-m","60","-A","Mozilla/5.0","-H","X-Requested-With: XMLHttpRequest","-X","POST","-d",f"ZiOrder={z}&PaginalZiNum=50&ImageSize=36",B],capture_output=True).stdout
    open(p,'wb').write(h)
with ThreadPoolExecutor(8) as ex: list(ex.map(g,range(int(sys.argv[1]),int(sys.argv[2]))))
print('done')
