import asyncio, sys, re, json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=True, args=["--no-sandbox"])
        pg = await b.new_page()
        caught=[]
        pg.on("response", lambda r: caught.append(r.url) if "api" in r.url or "ndownloader" in r.url else None)
        for k in sys.argv[1:]:
            await pg.goto(f"https://figshare.com/s/{k}", wait_until="networkidle", timeout=60000)
            await pg.wait_for_timeout(5000)
            html = await pg.content()
            print(k, await pg.title())
            print(sorted(set(re.findall(r'ndownloader/files/\d+[^"\s<]*', html)))[:5])
            print(sorted(set(re.findall(r'[\w\-]+\.(?:pth|zip|tar)', html)))[:10])
        print([u for u in caught][:20])
        await b.close()
asyncio.run(main())
