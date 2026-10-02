import asyncio, sys
from playwright.async_api import async_playwright
# Figshare private-link keys redacted for the public copy; supply (key, file_id, name) yourself.
items=[("<FIGSHARE_PRIVATE_LINK_KEY>","<FILE_ID>","moco_model_last.pth"),("<FIGSHARE_PRIVATE_LINK_KEY>","<FILE_ID>","val_max_val_acc.pth")]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=True, args=["--no-sandbox"])
        ctx = await b.new_context(accept_downloads=True)
        pg = await ctx.new_page()
        for k,f,name in items:
            await pg.goto(f"https://figshare.com/s/{k}", wait_until="networkidle", timeout=60000)
            async with pg.expect_download(timeout=1800000) as di:
                await pg.evaluate(f"window.location.href='https://figshare.com/ndownloader/files/{f}?private_link={k}'")
            d = await di.value
            await d.save_as(f"weights/{name}")
            print("saved", name, flush=True)
        await b.close()
asyncio.run(main())
