import asyncio,sys
from playwright.async_api import async_playwright
async def main(urls,outdir):
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"]); pg=await b.new_page(user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36')
        for u,name in urls:
            try:
                r=await pg.goto(u,timeout=45000); await pg.wait_for_timeout(1500)
                open(f'{outdir}/{name}.html','w').write(await pg.content()); print(name,r.status if r else None)
            except Exception as e: print(name,'ERR',str(e)[:100])
        await b.close()
args=sys.argv[2:]; asyncio.run(main([(a.split('|')[0],a.split('|')[1]) for a in args],sys.argv[1]))
