import asyncio, sys, re
from playwright.async_api import async_playwright
async def main(q, out):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page()
        await pg.goto("https://inscription.asdc.sinica.edu.tw/expl_search.php", timeout=60000)
        await pg.fill("#yan", q); await pg.dispatch_event("#yan","change")
        await pg.check("input[name=bookNum][value='101']")
        async with pg.expect_navigation(timeout=60000):
            await pg.click("input[type=submit]")
        await pg.wait_for_timeout(1500)
        try:
            async with pg.expect_navigation(timeout=30000):
                await pg.select_option("select[name=_pieceLen]", index=2)
        except Exception as e: print("pl",e)
        html = await pg.content()
        open(out+".p1.html","w").write(html)
        rows=[]; seen=set()
        for n in range(2000):
            t = await pg.inner_text("body")
            for line in t.split("\n"):
                if "\t" in line and "甲骨文合集" in line and line not in seen:
                    seen.add(line); rows.append(line)
            nxt = pg.locator("input[value='下頁']")
            if await nxt.count()==0: break
            try:
                async with pg.expect_navigation(timeout=30000):
                    await nxt.first.click()
            except Exception as e:
                break
        open(out+".tsv","w").write("\n".join(rows))
        print(len(rows))
        await b.close()
asyncio.run(main(sys.argv[1], sys.argv[2]))
