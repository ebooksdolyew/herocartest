import asyncio, sys
from pathlib import Path
from playwright.async_api import async_playwright

HERE = Path("/tmp/claude-0/-home-user-herocartest/e16f68ff-2bb3-50f1-8553-e89ebf72c043/scratchpad")
INPUT_HTML = HERE / "carrossel-studio-g85.html"
OUT = HERE / (sys.argv[1] if len(sys.argv) > 1 else "slides")
OUT.mkdir(parents=True, exist_ok=True)
SCALE = float(sys.argv[2]) if len(sys.argv) > 2 else 1080/420
TOTAL = 15
VIEW_W, VIEW_H = 420, 525

async def run():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg = await b.new_page(viewport={"width":VIEW_W,"height":VIEW_H}, device_scale_factor=SCALE)
        await pg.goto(INPUT_HTML.as_uri(), wait_until="load")
        try: await pg.evaluate("document.fonts.ready")
        except Exception: pass
        await pg.wait_for_timeout(3000)
        await pg.evaluate("""() => {
            document.querySelectorAll('.ig-header,.ig-dots,.ig-actions,.ig-caption').forEach(el=>el.style.display='none');
            const f=document.querySelector('.ig-frame');
            f.style.cssText='width:420px;height:525px;max-width:none;border-radius:0;box-shadow:none;overflow:hidden;margin:0;';
            const v=document.querySelector('.carousel-viewport');
            v.style.cssText='width:420px;height:525px;overflow:hidden;cursor:default;position:relative;';
            document.body.style.cssText='padding:0;margin:0;display:block;overflow:hidden;background:#000;';
        }""")
        await pg.wait_for_timeout(500)
        for i in range(TOTAL):
            await pg.evaluate("""(idx)=>{const t=document.querySelector('.carousel-track');
                t.style.transition='none';t.style.transform='translateX('+(-idx*420)+'px)';}""", i)
            await pg.wait_for_timeout(320)
            await pg.screenshot(path=str(OUT/f"slide_{i+1:02d}.png"),
                                clip={"x":0,"y":0,"width":VIEW_W,"height":VIEW_H})
            print("slide", i+1, flush=True)
        await b.close()

asyncio.run(run())
