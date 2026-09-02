import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

OUT = Path("/tmp/claude-0/-home-user-herocartest/e16f68ff-2bb3-50f1-8553-e89ebf72c043/scratchpad/shots2")
OUT.mkdir(parents=True, exist_ok=True)
BASE = "http://localhost:8099"

PREP = """() => {
  document.querySelectorAll('.r,.r-l,.r-r,.r-s,.lines').forEach(e=>e.classList.add('in'));
  document.querySelectorAll('.grain,.vignette,.spotlight,.progress,.ck').forEach(e=>e.remove());
  if(!document.getElementById('__noanim')){
    const s=document.createElement('style'); s.id='__noanim';
    s.textContent='*{animation-duration:0s!important;transition-duration:0s!important}'+
      '.r,.r-l,.r-r,.r-s,.lines{opacity:1!important;transform:none!important;filter:none!important}';
    document.head.appendChild(s);
  }
}"""

JOBS = [
  ("/index.html", (1440,900), [
     ("home-hero", None), ("home-sobre","#sobre"), ("home-servicos","#servicos"),
     ("home-processo","#processo"), ("home-galeria","#galeria"), ("home-videos","#videos"),
     ("home-perfil","#perfil"), ("home-avaliacoes","#avaliacoes"), ("home-estrutura","#estrutura"),
     ("home-faq","#faq"), ("home-contato","#contato"),
  ]),
  ("/servicos/vitrificacao-ceramica.html", (1440,900), [("svc-vitri-1",None),("svc-vitri-2","__scroll:1000")]),
  ("/servicos/ppf-paint-protection-film.html", (1440,900), [("svc-ppf-1",None),("svc-ppf-2","__scroll:1000")]),
  ("/servicos/pelicula-window-blue.html", (1440,900), [("svc-pel-1",None),("svc-pel-2","__scroll:1000")]),
  ("/servicos/lavagem-tecnica.html", (1440,900), [("svc-lav-1",None),("svc-lav-2","__scroll:1000")]),
  ("/politica-de-privacidade.html", (1440,900), [("priv",None)]),
  ("/404.html", (1440,900), [("e404",None)]),
  ("/index.html", (390,844), [("mob-hero",None),("mob-servicos","#servicos"),("mob-galeria","#galeria"),("mob-contato","#contato")]),
  ("/index.html", (834,1112), [("tab-hero",None),("tab-galeria","#galeria"),("tab-avaliacoes","#avaliacoes")]),
]

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        ctx = await b.new_context(viewport={"width":1440,"height":900}, device_scale_factor=2)
        await ctx.add_init_script("try{localStorage.setItem('g85:consent:v1','recusado')}catch(e){}")
        for url, vp, shots in JOBS:
            pg = await ctx.new_page()
            await pg.set_viewport_size({"width":vp[0],"height":vp[1]})
            await pg.goto(BASE+url, wait_until="domcontentloaded")
            await pg.wait_for_timeout(2500)
            try:
                await pg.evaluate("document.fonts.ready")
            except Exception: pass
            await pg.evaluate(PREP)
            await pg.wait_for_timeout(600)
            for name, sel in shots:
                try:
                    if sel is None:
                        await pg.evaluate("window.scrollTo(0,0)")
                    elif sel.startswith("__scroll:"):
                        await pg.evaluate("window.scrollTo(0,%s)" % sel.split(":")[1])
                    else:
                        await pg.evaluate("""(s)=>{const el=document.querySelector(s);
                          if(el){const y=el.getBoundingClientRect().top+window.scrollY-96;window.scrollTo(0,y);}}""", sel)
                    await pg.wait_for_timeout(900)
                    await pg.evaluate(PREP)
                    await pg.wait_for_timeout(700)
                    await pg.screenshot(path=str(OUT/f"{name}.png"))
                    print("OK", name, flush=True)
                except Exception as e:
                    print("ERR", name, e, flush=True)
            await pg.close()
        await b.close()

asyncio.run(main())
