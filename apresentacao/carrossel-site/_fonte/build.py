# -*- coding: utf-8 -*-
import base64
from pathlib import Path

HERE = Path("/tmp/claude-0/-home-user-herocartest/e16f68ff-2bb3-50f1-8553-e89ebf72c043/scratchpad")
PREP = HERE / "prep"

def uri(name):
    p = PREP / name
    mime = "image/png" if p.suffix == ".png" else "image/jpeg"
    return "data:%s;base64,%s" % (mime, base64.b64encode(p.read_bytes()).decode())

IMG = {p.stem: uri(p.name) for p in PREP.iterdir() if p.suffix in (".jpg", ".png")}

# ---------------------------------------------------------------- tokens
INK      = "#0A0A0B"
INK_2    = "#121215"
PAPER    = "#F4F2EE"
DIM      = "rgba(244,242,238,.58)"
DIM_D    = "rgba(10,10,11,.55)"
GOLD     = "#F2C230"
GOLD_L   = "#FFD966"
GOLD_D   = "#C99A12"
LIGHT_BG = "#F4F2EE"
LIGHT_BD = "#E2DDD3"
BLOOD    = "#C8102E"

TOTAL = 15

GRAIN = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E"
         "%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='4'/%3E"
         "%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)'/%3E%3C/svg%3E\")")

CHECKER = ("background-image:linear-gradient(45deg,#F4F2EE 25%,transparent 25%,transparent 75%,#F4F2EE 75%),"
           "linear-gradient(45deg,#F4F2EE 25%,transparent 25%,transparent 75%,#F4F2EE 75%);"
           "background-size:8px 8px;background-position:0 0,4px 4px;")
CHECKER_D = CHECKER.replace("#F4F2EE", "#141416")

# ---------------------------------------------------------------- helpers
def progress(i, light):
    pct = ((i + 1) / TOTAL) * 100
    track = "rgba(10,10,11,.10)" if light else "rgba(255,255,255,.12)"
    fill  = GOLD_D if light else GOLD
    lab   = "rgba(10,10,11,.32)" if light else "rgba(255,255,255,.38)"
    return ("<div style=\"position:absolute;bottom:0;left:0;right:0;padding:16px 26px 18px;z-index:20;"
            "display:flex;align-items:center;gap:10px;\">"
            "<div style=\"flex:1;height:3px;background:%s;border-radius:2px;overflow:hidden;\">"
            "<div style=\"height:100%%;width:%.2f%%;background:%s;border-radius:2px;\"></div></div>"
            "<span class=\"sans\" style=\"font-size:10px;color:%s;font-weight:600;letter-spacing:.06em;\">%02d/%d</span>"
            "</div>") % (track, pct, fill, lab, i + 1, TOTAL)

def arrow(light):
    bg = "rgba(10,10,11,.05)" if light else "rgba(255,255,255,.06)"
    st = "rgba(10,10,11,.28)" if light else "rgba(255,255,255,.34)"
    return ("<div style=\"position:absolute;right:0;top:0;bottom:0;width:44px;z-index:19;display:flex;"
            "align-items:center;justify-content:center;background:linear-gradient(to right,transparent,%s);\">"
            "<svg width='20' height='20' viewBox='0 0 24 24' fill='none'>"
            "<path d='M9 6l6 6-6 6' stroke='%s' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'/>"
            "</svg></div>") % (bg, st)

def over(txt, color=GOLD):
    return ("<span class=\"sans\" style=\"display:inline-block;font-size:8.5px;font-weight:700;letter-spacing:.24em;"
            "color:%s;text-transform:uppercase;\">%s</span>") % (color, txt)

def checkerbar(light=False, w="46px"):
    css = CHECKER_D if light else CHECKER
    return "<div style=\"width:%s;height:8px;%s\"></div>" % (w, css)

def browser(src, w=None, style="", url="www.studiog85.com", dark=True, bar=13, radius=7):
    dot = "rgba(255,255,255,.20)" if dark else "rgba(0,0,0,.18)"
    barbg = "#1B1B1F" if dark else "#DCD7CD"
    pill = "rgba(255,255,255,.07)" if dark else "rgba(0,0,0,.05)"
    txt = "rgba(255,255,255,.34)" if dark else "rgba(0,0,0,.34)"
    width = ("width:%s;" % w) if w else ""
    return ("<div style=\"%s%sborder-radius:%dpx;overflow:hidden;background:%s;"
            "box-shadow:0 20px 44px rgba(0,0,0,.55),0 0 0 1px rgba(255,255,255,.07);\">"
            "<div style=\"height:%dpx;background:%s;display:flex;align-items:center;gap:3.5px;padding:0 7px;\">"
            "<span style=\"width:4px;height:4px;border-radius:50%%;background:%s\"></span>"
            "<span style=\"width:4px;height:4px;border-radius:50%%;background:%s\"></span>"
            "<span style=\"width:4px;height:4px;border-radius:50%%;background:%s\"></span>"
            "<div style=\"flex:1;height:%dpx;margin-left:5px;background:%s;border-radius:9px;display:flex;"
            "align-items:center;justify-content:center;\">"
            "<span class=\"sans\" style=\"font-size:5.5px;letter-spacing:.05em;color:%s\">%s</span></div></div>"
            "<img src=\"%s\" style=\"display:block;width:100%%;\">"
            "</div>") % (width, style, radius, barbg, bar, barbg, dot, dot, dot,
                         bar - 5, pill, txt, url, src)

def shot(src, w, style="", radius=5, ring="rgba(255,255,255,.09)", shadow="0 16px 34px rgba(0,0,0,.5)"):
    return ("<div style=\"width:%s;%sborder-radius:%dpx;overflow:hidden;box-shadow:%s,0 0 0 1px %s;\">"
            "<img src=\"%s\" style=\"display:block;width:100%%;\"></div>") % (w, style, radius, shadow, ring, src)

def tag(txt, light=False):
    c = GOLD_D if light else GOLD_L
    bg = "rgba(201,154,18,.10)" if light else "rgba(242,194,48,.10)"
    bd = "rgba(201,154,18,.25)" if light else "rgba(242,194,48,.22)"
    return ("<span class=\"sans\" style=\"font-size:8px;font-weight:600;letter-spacing:.09em;padding:3.5px 8px;"
            "border:1px solid %s;background:%s;border-radius:20px;color:%s;white-space:nowrap;\">%s</span>") % (bd, bg, c, txt)

def caption(label, text, light=False):
    c1 = GOLD_D if light else GOLD
    c2 = "rgba(10,10,11,.50)" if light else DIM
    return ("<div style=\"margin-top:7px\">"
            "<div class=\"sans\" style=\"font-size:8px;font-weight:700;letter-spacing:.18em;color:%s;text-transform:uppercase\">%s</div>"
            "<div class=\"sans\" style=\"font-size:9.5px;line-height:1.4;color:%s;margin-top:2px\">%s</div></div>") % (c1, label, c2, text)

def slide(i, bg, inner, light=False, extra=""):
    last = (i == TOTAL - 1)
    return ("<div class=\"slide\" style=\"background:%s;%s\">"
            "<div class=\"grain\"></div>%s%s%s%s</div>") % (
        bg, extra, inner, "" if last else arrow(light), progress(i, light), "")

def lockup(dark=True, size=26, name=True):
    logo = IMG["logo-paper"] if dark else IMG["logo-g85"]
    col = PAPER if dark else INK
    sub = "rgba(244,242,238,.42)" if dark else "rgba(10,10,11,.45)"
    nm = ("<div><div class=\"sans\" style=\"font-size:9.5px;font-weight:700;letter-spacing:.14em;color:%s\">STUDIO G85</div>"
          "<div class=\"sans\" style=\"font-size:7.5px;letter-spacing:.14em;color:%s\">FORTALEZA · CE</div></div>") % (col, sub)
    return ("<div style=\"display:flex;align-items:center;gap:9px\">"
            "<img src=\"%s\" style=\"width:%dpx;height:%dpx;object-fit:contain\">%s</div>") % (logo, size, size, nm if name else "")

# ================================================================ SLIDES
PAD = "position:absolute;inset:0;padding:28px 30px 54px;z-index:5;display:flex;flex-direction:column;"

S = []

# ---------- 01 · CAPA
S.append(dict(light=False, bg=f"radial-gradient(120% 90% at 78% 8%,#1C1A16 0%,{INK} 58%)", inner=f"""
<div style="position:absolute;left:0;right:0;top:52px;text-align:center;z-index:1;">
  <div class="serif" style="font-size:63px;font-weight:900;letter-spacing:-.05em;line-height:.82;
       color:transparent;-webkit-text-stroke:1.1px rgba(242,194,48,.30);">PORTFÓLIO</div>
</div>
<div style="{PAD}">
  <div style="display:flex;align-items:center;gap:9px;">
    {checkerbar()}
    {over("Site institucional · 2026")}
  </div>
  <div style="margin-top:44px;transform:rotate(-2.2deg);">
    {browser(IMG['home-hero'], w="100%")}
  </div>
  <div style="margin-top:auto;">
    <div class="serif" style="font-size:23px;font-weight:800;line-height:1.06;letter-spacing:-.025em;color:{PAPER};text-transform:uppercase;">
      Não vendemos brilho.
    </div>
    <div class="serif" style="font-size:23px;font-weight:800;line-height:1.06;letter-spacing:-.025em;color:{PAPER};text-transform:uppercase;">
      Vendemos <span style="color:{GOLD}">tempo de vida</span>.
    </div>
    <div style="height:1px;background:rgba(255,255,255,.10);margin:14px 0 12px;"></div>
    <div style="display:flex;align-items:center;justify-content:space-between;">
      {lockup(True)}
      <span class="sans" style="font-size:8px;letter-spacing:.16em;color:rgba(244,242,238,.34)">ARRASTA →</span>
    </div>
  </div>
</div>"""))

# ---------- 02 · O PROJETO
def stat(n, t):
    return f"""<div style="border:1px solid {LIGHT_BD};border-radius:8px;padding:11px 12px;background:#FBFAF7;">
      <div class="serif" style="font-size:26px;font-weight:800;line-height:1;color:{INK};letter-spacing:-.03em">{n}</div>
      <div class="sans" style="font-size:8px;font-weight:600;letter-spacing:.13em;color:rgba(10,10,11,.45);margin-top:5px;text-transform:uppercase">{t}</div>
    </div>"""

S.append(dict(light=True, bg=LIGHT_BG, inner=f"""
<div style="{PAD}">
  <div style="display:flex;align-items:center;gap:9px;">{checkerbar(True)}{over("O projeto", GOLD_D)}</div>
  <div class="serif" style="margin-top:14px;font-size:26px;font-weight:800;line-height:1.02;letter-spacing:-.03em;color:{INK};text-transform:uppercase;">
    Do zero.<br>Sem <span style="color:{GOLD_D}">template</span>.
  </div>
  <div class="sans" style="margin-top:10px;font-size:10.5px;line-height:1.5;color:rgba(10,10,11,.58);max-width:290px;">
    HTML, CSS e JavaScript puro. Sem construtor de página, sem tema pronto, sem plugin.
  </div>
  <div style="margin-top:16px;display:grid;grid-template-columns:1fr 1fr;gap:8px;">
    {stat("07","páginas")}{stat("20","veículos reais")}{stat("09","vídeos próprios")}{stat("00","imagens de banco")}
  </div>
  <div style="margin-top:auto;display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;">
    {shot(IMG['home-servicos'],"100%",radius=4,ring="rgba(0,0,0,.10)",shadow="0 6px 16px rgba(0,0,0,.16)")}
    {shot(IMG['home-galeria'],"100%",radius=4,ring="rgba(0,0,0,.10)",shadow="0 6px 16px rgba(0,0,0,.16)")}
    {shot(IMG['home-avaliacoes'],"100%",radius=4,ring="rgba(0,0,0,.10)",shadow="0 6px 16px rgba(0,0,0,.16)")}
  </div>
</div>"""))

# ---------- 03 · FONTES & CORES
def fontrow(sample, sample_style, name, role, border=True):
    bd = "border-bottom:1px solid rgba(255,255,255,.09);" if border else ""
    return f"""<div style="display:flex;align-items:center;gap:14px;padding:11px 0;{bd}">
      <div style="width:104px;flex:none;{sample_style}">{sample}</div>
      <div>
        <div class="sans" style="font-size:9.5px;font-weight:700;letter-spacing:.14em;color:{PAPER};text-transform:uppercase">{name}</div>
        <div class="sans" style="font-size:8.5px;color:{DIM};margin-top:1px">{role}</div>
      </div>
    </div>"""

def sw(hexv, name):
    ring = "rgba(255,255,255,.16)"
    return f"""<div style="text-align:center">
      <div style="height:36px;border-radius:6px;background:{hexv};box-shadow:inset 0 0 0 1px {ring}"></div>
      <div class="sans" style="font-size:7px;font-weight:700;letter-spacing:.05em;color:{PAPER};margin-top:5px">{hexv}</div>
      <div class="sans" style="font-size:6.5px;letter-spacing:.09em;color:rgba(244,242,238,.38);margin-top:1px;text-transform:uppercase">{name}</div>
    </div>"""

S.append(dict(light=False, bg=f"linear-gradient(170deg,{INK_2} 0%,{INK} 60%)", inner=f"""
<div style="{PAD}">
  <div style="display:flex;align-items:center;gap:9px;">{checkerbar()}{over("Identidade visual")}</div>
  <div class="serif" style="margin-top:13px;font-size:26px;font-weight:800;line-height:1;letter-spacing:-.03em;color:{PAPER};text-transform:uppercase;">
    Fontes <span style="color:{GOLD}">&</span> cores
  </div>
  <div style="margin-top:12px;">
    {fontrow('<span class="serif" style="font-size:31px;font-weight:900;color:'+PAPER+';letter-spacing:-.03em">Aa 85</span>','','Montserrat','Títulos, números e menu · 400–900')}
    {fontrow('<span class="sans" style="font-size:27px;font-weight:400;color:'+PAPER+'">Aa 85</span>','','Inter','Corpo de texto e listas · 300–700')}
    {fontrow('<span class="script" style="font-size:29px;font-weight:700;color:'+GOLD+'">studio g85</span>','','Dancing Script','Assinatura da marca',border=False)}
  </div>
  <div style="margin-top:auto;">
    <div class="sans" style="font-size:8px;font-weight:700;letter-spacing:.2em;color:{DIM};margin-bottom:9px;text-transform:uppercase">Paleta</div>
    <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:6px;">
      {sw("#040404","Ink")}{sw("#0E0E10","Palco")}{sw("#F4F2EE","Papel")}{sw("#F2C230","Ouro")}{sw("#C99A12","Ouro fosco")}{sw("#C8102E","Alerta")}
    </div>
  </div>
</div>"""))

def head(over_txt, title_html, sub, light):
    c = INK if light else PAPER
    d = "rgba(10,10,11,.55)" if light else DIM
    return f"""<div style="display:flex;align-items:center;gap:9px;">{checkerbar(light)}{over(over_txt, GOLD_D if light else GOLD)}</div>
  <div class="serif" style="margin-top:12px;font-size:23px;font-weight:800;line-height:1.02;letter-spacing:-.03em;color:{c};text-transform:uppercase;">{title_html}</div>
  <div class="sans" style="margin-top:8px;font-size:9.5px;line-height:1.45;color:{d};max-width:300px;">{sub}</div>"""

def chip(txt, light):
    c = GOLD_D if light else GOLD
    return f"""<span class="sans" style="font-size:7.5px;font-weight:700;letter-spacing:.17em;color:{c};text-transform:uppercase">{txt}</span>"""

def framed(src, w, light, rot=0, radius=5):
    ring = "rgba(0,0,0,.12)" if light else "rgba(255,255,255,.10)"
    sh = "0 14px 30px rgba(0,0,0,.30)" if light else "0 14px 30px rgba(0,0,0,.55)"
    tr = f"transform:rotate({rot}deg);" if rot else ""
    return f"""<div style="width:{w};{tr}border-radius:{radius}px;overflow:hidden;box-shadow:{sh},0 0 0 1px {ring};">
      <img src="{src}" style="display:block;width:100%;"></div>"""

# ---------- 04 · HOME / ABERTURA
S.append(dict(light=True, bg=LIGHT_BG, inner=f"""
<div style="{PAD}">
  {head("Página 01 · Home", 'A primeira<br>dobra', "Vídeo do box rodando em loop, promessa em duas linhas e dois caminhos: conhecer ou orçar.", True)}
  <div style="margin-top:14px;display:flex;gap:5px;flex-wrap:wrap">{tag("VÍDEO EM WEBM",True)}{tag("MENU FIXO",True)}{tag("FAIXA DE SERVIÇOS",True)}</div>
  <div style="margin-top:auto;">
    {browser(IMG['home-hero'], w="100%", dark=True)}
    <div class="sans" style="margin-top:9px;font-size:8px;letter-spacing:.15em;color:rgba(10,10,11,.38);text-transform:uppercase">www.studiog85.com</div>
  </div>
</div>"""))

# ---------- 05 · HOME / SOBRE + SERVIÇOS
S.append(dict(light=False, bg=f"radial-gradient(110% 80% at 15% 92%,#191713 0%,{INK} 62%)", inner=f"""
<div style="{PAD}">
  {head("Home · seções 02 e 03", 'Argumento<br>e catálogo', "A tese antes da venda: primeiro por que proteger, depois as quatro frentes em acordeão.", False)}
  <div style="position:relative;margin-top:16px;height:290px;">
    <div style="position:absolute;left:0;top:0;width:232px;">{chip("Sobre nós", False)}<div style="margin-top:5px">{framed(IMG['home-sobre'],"100%",False,rot=-2)}</div></div>
    <div style="position:absolute;right:0;top:148px;width:240px;text-align:right">{chip("Nossos serviços", False)}<div style="margin-top:5px">{framed(IMG['home-servicos'],"100%",False,rot=2)}</div></div>
  </div>
</div>"""))

# ---------- 06 · HOME / PROCESSO + GALERIA + VÍDEOS
S.append(dict(light=True, bg=LIGHT_BG, inner=f"""
<div style="{PAD}">
  {head("Home · seções 04 a 06", 'Prova<br>em três camadas', "Etapas numeradas, 20 veículos reais no hall da fama e vídeos que ninguém edita.", True)}
  <div style="margin-top:14px;">{chip("Como trabalhamos", True)}<div style="margin-top:5px">{framed(IMG['home-processo'],"100%",True)}</div></div>
  <div style="margin-top:auto;display:grid;grid-template-columns:1fr 1fr;gap:8px;">
    <div>{chip("Galeria", True)}<div style="margin-top:5px">{framed(IMG['home-galeria'],"100%",True)}</div></div>
    <div>{chip("Vídeos", True)}<div style="margin-top:5px">{framed(IMG['home-videos'],"100%",True)}</div></div>
  </div>
</div>"""))

# ---------- 07 · HOME / PERFIL + AVALIAÇÕES
S.append(dict(light=False, bg=f"radial-gradient(110% 80% at 85% 10%,#1B1814 0%,{INK} 60%)", inner=f"""
<div style="{PAD}">
  {head("Home · seções 07 e 08", 'Filtro<br>e reputação', "Duas colunas dizendo para quem o serviço não é — e nota 5,0 no Google logo abaixo.", False)}
  <div style="margin-top:16px;">{chip("É pra você se… / não é pra você se…", False)}<div style="margin-top:5px">{framed(IMG['home-perfil'],"100%",False)}</div></div>
  <div style="margin-top:auto;display:flex;align-items:flex-end;gap:10px;">
    <div style="flex:1">{chip("Avaliações", False)}<div style="margin-top:5px">{framed(IMG['home-avaliacoes'],"100%",False)}</div></div>
    <div style="width:74px;flex:none;text-align:center;border:1px solid rgba(242,194,48,.28);border-radius:8px;padding:9px 4px;background:rgba(242,194,48,.07)">
      <div class="serif" style="font-size:24px;font-weight:800;color:{GOLD};line-height:1">5,0</div>
      <div class="sans" style="font-size:8px;color:{GOLD_L};margin-top:2px">★★★★★</div>
      <div class="sans" style="font-size:6.5px;letter-spacing:.1em;color:{DIM};margin-top:3px;text-transform:uppercase">no Google</div>
    </div>
  </div>
</div>"""))

# ---------- 08 · HOME / ESTRUTURA + FAQ + CONTATO
S.append(dict(light=True, bg=LIGHT_BG, inner=f"""
<div style="{PAD}">
  {head("Home · seções 09 a 11", 'Fechamento<br>sem fricção', "O box por dentro, sete dúvidas respondidas e um formulário de quatro campos que abre o WhatsApp pronto.", True)}
  <div style="margin-top:16px;">{chip("Nossa estrutura", True)}<div style="margin-top:5px">{framed(IMG['home-estrutura'],"100%",True)}</div></div>
  <div style="margin-top:auto;display:grid;grid-template-columns:1fr 1fr;gap:8px;">
    <div>{chip("Dúvidas", True)}<div style="margin-top:5px">{framed(IMG['home-faq'],"100%",True)}</div></div>
    <div>{chip("Contato", True)}<div style="margin-top:5px">{framed(IMG['home-contato'],"100%",True)}</div></div>
  </div>
</div>"""))

# ---------- 09 a 12 · PÁGINAS DE SERVIÇO
def svc_slide(light, kicker, title, sub, tags, big, small, url):
    bgd = f"radial-gradient(110% 80% at 20% 6%,#1A1713 0%,{INK} 62%)"
    return dict(light=light, bg=(LIGHT_BG if light else bgd), inner=f"""
<div style="{PAD}">
  {head(kicker, title, sub, light)}
  <div style="margin-top:12px;display:flex;gap:5px;flex-wrap:wrap">{''.join(tag(t, light) for t in tags)}</div>
  <div style="margin-top:auto;position:relative;">
    {browser(IMG[big], w="100%", url=url)}
    <div style="position:absolute;right:-6px;bottom:-16px;width:132px;">{framed(IMG[small],"100%",light,rot=-2.5,radius=4)}</div>
  </div>
</div>""")

S.append(svc_slide(False, "Página 02 · Serviço", 'Vitrificação<br>cerâmica',
    "Camada de sacrifício sobre pintura, vidros e couro. Página própria, com FAQ e formulário já preenchido.",
    ["3 OU 5 ANOS", "SEO PRÓPRIO", "FORMULÁRIO PRÉ-SELECIONADO"],
    "svc-vitri-1", "svc-vitri-2", "studiog85.com/vitrificacao"))

S.append(svc_slide(True, "Página 03 · Serviço", 'PPF — paint<br>protection film',
    "Película transparente nas áreas que apanham primeiro. Corte computadorizado, sem borda aparente.",
    ["AUTORREGENERATIVO", "TRANSPARENTE E FUMÊ", "APLICAÇÃO INTERNA"],
    "svc-ppf-1", "svc-ppf-2", "studiog85.com/ppf"))

S.append(svc_slide(False, "Página 04 · Serviço", 'Película<br>Window Blue',
    "Calor, UV e visibilidade noturna resolvidos na mesma película — com garantia vitalícia nacional.",
    ["GARANTIA VITALÍCIA", "CERTIFICAÇÃO UV", "SEM BOLHA"],
    "svc-pel-1", "svc-pel-2", "studiog85.com/pelicula"))

S.append(svc_slide(True, "Página 05 · Serviço", 'Lavagem<br>técnica',
    "A manutenção que preserva a proteção já aplicada — método e produto certos, não esponja de lava-jato.",
    ["MANUTENÇÃO", "HIGIENIZAÇÃO INTERNA", "POLIMENTO"],
    "svc-lav-1", "svc-lav-2", "studiog85.com/lavagem"))

# ---------- 13 · PÁGINAS DE APOIO + BASTIDORES
def line(k, v):
    return f"""<div style="display:flex;gap:9px;align-items:flex-start;padding:7px 0;border-bottom:1px solid rgba(255,255,255,.08)">
      <span style="color:{GOLD};font-size:9px;line-height:1.4">◆</span>
      <div><span class="sans" style="font-size:9.5px;font-weight:600;color:{PAPER}">{k}</span>
      <span class="sans" style="font-size:9.5px;color:{DIM}"> — {v}</span></div></div>"""

S.append(dict(light=False, bg=f"linear-gradient(180deg,{INK_2} 0%,{INK} 70%)", inner=f"""
<div style="{PAD}">
  {head("Páginas 06 e 07 · Apoio", 'O que ninguém<br>vê — e conta', "Privacidade e erro 404 tratados como página de verdade, não como sobra.", False)}
  <div style="margin-top:14px;display:grid;grid-template-columns:1fr 1fr;gap:9px;">
    <div>{chip("Privacidade", False)}<div style="margin-top:5px">{framed(IMG['priv'],"100%",False)}</div></div>
    <div>{chip("Erro 404", False)}<div style="margin-top:5px">{framed(IMG['e404'],"100%",False)}</div></div>
  </div>
  <div style="margin-top:auto;">
    {line("LGPD", "banner com Consent Mode v2, nada carrega antes do aceite")}
    {line("SEO", "canonical, Open Graph e JSON-LD em todas as páginas")}
    {line("Performance", "imagens em WebP, vídeos em WebM, zero framework")}
  </div>
</div>"""))

# ---------- 14 · DISPOSITIVOS
def phone(src, w):
    return f"""<div style="width:{w};border:3px solid #24242A;border-radius:15px;background:#24242A;overflow:hidden;
      box-shadow:0 18px 34px rgba(0,0,0,.38),0 0 0 1px rgba(0,0,0,.12);position:relative;">
      <div style="position:absolute;left:50%;top:4px;transform:translateX(-50%);width:26%;height:3.5px;border-radius:4px;background:#0A0A0B;z-index:2"></div>
      <img src="{src}" style="display:block;width:100%;border-radius:12px;"></div>"""

def tablet(src, w):
    return f"""<div style="width:{w};border:4px solid #26262C;border-radius:11px;background:#26262C;overflow:hidden;
      box-shadow:0 20px 38px rgba(0,0,0,.38),0 0 0 1px rgba(0,0,0,.12);">
      <img src="{src}" style="display:block;width:100%;border-radius:7px;"></div>"""

S.append(dict(light=True, bg=f"radial-gradient(110% 80% at 50% 0%,#FFFDF8 0%,{LIGHT_BG} 55%)", inner=f"""
<div style="{PAD}">
  {head("Responsivo", 'Mesma história,<br>três telas', "Do desktop de 1440px ao celular na fila do semáforo — nenhum bloco quebra, nenhum texto encolhe.", True)}
  <div style="position:relative;margin-top:auto;height:250px;">
    <div style="position:absolute;left:-4px;top:2px;width:276px;">{browser(IMG['home-hero'], w="100%", radius=6)}</div>
    <div style="position:absolute;right:62px;top:76px;width:126px;">{tablet(IMG['tab-hero'],"100%")}</div>
    <div style="position:absolute;right:-2px;top:118px;width:80px;">{phone(IMG['mob-hero'],"100%")}</div>
  </div>
  <div style="display:flex;gap:14px;margin-top:10px;">
    <span class="sans" style="font-size:7.5px;font-weight:700;letter-spacing:.15em;color:rgba(10,10,11,.42)">DESKTOP 1440</span>
    <span class="sans" style="font-size:7.5px;font-weight:700;letter-spacing:.15em;color:rgba(10,10,11,.42)">TABLET 834</span>
    <span class="sans" style="font-size:7.5px;font-weight:700;letter-spacing:.15em;color:rgba(10,10,11,.42)">MOBILE 390</span>
  </div>
</div>"""))

# ---------- 15 · CTA
S.append(dict(light=True, bg=f"linear-gradient(165deg,{GOLD_D} 0%,{GOLD} 52%,{GOLD_L} 100%)", inner=f"""
<div style="{PAD}justify-content:center;align-items:center;text-align:center;">
  <img src="{IMG['logo-g85']}" style="width:56px;height:56px;object-fit:contain;opacity:.92">
  <div class="serif" style="margin-top:16px;font-size:27px;font-weight:800;line-height:1.02;letter-spacing:-.03em;color:{INK};text-transform:uppercase;">
    O site está<br>no ar.
  </div>
  <div class="sans" style="margin-top:10px;font-size:10.5px;line-height:1.5;color:rgba(10,10,11,.62);max-width:250px;">
    Passa lá, rola até o fim e repara nos detalhes que não aparecem em print.
  </div>
  <div style="margin-top:18px;display:inline-flex;align-items:center;gap:7px;padding:11px 24px;background:{INK};
       color:{PAPER};border-radius:26px;">
    <span class="sans" style="font-size:11px;font-weight:700;letter-spacing:.06em;">WWW.STUDIOG85.COM</span>
  </div>
  <div style="margin-top:16px;display:flex;align-items:center;gap:8px;">
    {checkerbar(True, "30px")}
    <span class="script" style="font-size:19px;font-weight:700;color:{INK}">studio g85</span>
    {checkerbar(True, "30px")}
  </div>
  <div class="sans" style="margin-top:6px;font-size:8px;font-weight:700;letter-spacing:.2em;color:rgba(10,10,11,.5)">@STUDIO.G85 · FORTALEZA/CE</div>
</div>"""))

assert len(S) == TOTAL, f"esperado {TOTAL} slides, montados {len(S)}"

slides_html = "".join(slide(i, s["bg"], s["inner"], s["light"]) for i, s in enumerate(S))
dots = "".join('<span class="dot%s"></span>' % (" on" if i == 0 else "") for i in range(TOTAL))

CSS = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{background:#111113;font-family:'Inter',system-ui,sans-serif;display:flex;justify-content:center;
  align-items:flex-start;padding:26px 12px 46px;min-height:100vh}
.serif{font-family:'Montserrat',system-ui,sans-serif}
.sans{font-family:'Inter',system-ui,sans-serif}
.script{font-family:'Dancing Script',cursive}
.ig-frame{width:420px;max-width:420px;background:#000;border-radius:12px;overflow:hidden;
  box-shadow:0 24px 70px rgba(0,0,0,.6)}
.ig-header{display:flex;align-items:center;gap:10px;padding:11px 14px;border-bottom:1px solid #1e1e21}
.ig-avatar{width:32px;height:32px;border-radius:50%;background:#F2C230;display:flex;align-items:center;
  justify-content:center;overflow:hidden}
.ig-avatar img{width:24px;height:24px;object-fit:contain}
.carousel-viewport{width:420px;height:525px;overflow:hidden;position:relative;cursor:grab;background:#000;
  touch-action:pan-y}
.carousel-viewport:active{cursor:grabbing}
.carousel-track{display:flex;width:max-content;transition:transform .38s cubic-bezier(.22,1,.36,1)}
.slide{width:420px;height:525px;position:relative;overflow:hidden;flex:none}
.slide .grain{position:absolute;inset:0;z-index:2;pointer-events:none;opacity:.05;
  background-image:GRAINURL;background-size:200px 200px}
.ig-dots{display:flex;justify-content:center;gap:5px;padding:11px 0 4px}
.dot{width:5px;height:5px;border-radius:50%;background:#3a3a40}
.dot.on{background:#F2C230}
.ig-actions{display:flex;align-items:center;gap:15px;padding:6px 14px 2px}
.ig-caption{padding:6px 14px 15px}
img{-webkit-user-drag:none;user-select:none}
"""
CSS = CSS.replace("GRAINURL", GRAIN)

JS = """
(function(){
  var vp=document.querySelector('.carousel-viewport'),tr=document.querySelector('.carousel-track');
  var dots=[].slice.call(document.querySelectorAll('.dot')),n=TOTALN,i=0,x0=null,dx=0;
  function go(k){i=Math.max(0,Math.min(n-1,k));tr.style.transform='translateX('+(-i*420)+'px)';
    dots.forEach(function(d,j){d.classList.toggle('on',j===i)});}
  vp.addEventListener('pointerdown',function(e){x0=e.clientX;dx=0;tr.style.transition='none';vp.setPointerCapture(e.pointerId)});
  vp.addEventListener('pointermove',function(e){if(x0===null)return;dx=e.clientX-x0;
    tr.style.transform='translateX('+(-i*420+dx)+'px)'});
  function end(){if(x0===null)return;tr.style.transition='';
    if(dx<-45)go(i+1);else if(dx>45)go(i-1);else go(i);x0=null;dx=0;}
  vp.addEventListener('pointerup',end);vp.addEventListener('pointercancel',end);vp.addEventListener('pointerleave',end);
  document.addEventListener('keydown',function(e){if(e.key==='ArrowRight')go(i+1);if(e.key==='ArrowLeft')go(i-1)});
  go(0);
})();
""".replace("TOTALN", str(TOTAL))

ICON = ("<svg width='21' height='21' viewBox='0 0 24 24' fill='none' stroke='#f2f2f2' stroke-width='1.7' "
        "stroke-linecap='round' stroke-linejoin='round'>%s</svg>")
HEART = ICON % "<path d='M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l8.8 8.8 8.8-8.8a5.5 5.5 0 0 0 0-7.8z'/>"
COMM  = ICON % "<path d='M21 11.5a8.4 8.4 0 0 1-9 8.4 8.9 8.9 0 0 1-3.9-.9L3 20.5l1.5-4.4A8.4 8.4 0 0 1 12 3.1a8.4 8.4 0 0 1 9 8.4z'/>"
SEND  = ICON % "<path d='M22 2 11 13'/><path d='M22 2 15 22l-4-9-9-4 20-7z'/>"
MARK  = ICON % "<path d='M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z'/>"

HTML = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Carrossel · Studio G85</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&family=Dancing+Script:wght@600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="ig-frame">
  <div class="ig-header">
    <div class="ig-avatar"><img src="{IMG['logo-g85']}"></div>
    <div>
      <div style="font-size:12.5px;font-weight:600;color:#f2f2f2">studio.g85</div>
      <div style="font-size:10.5px;color:#8a8a90">Fortaleza · Ceará</div>
    </div>
  </div>
  <div class="carousel-viewport"><div class="carousel-track">{slides_html}</div></div>
  <div class="ig-dots">{dots}</div>
  <div class="ig-actions">{HEART}{COMM}{SEND}<span style="flex:1"></span>{MARK}</div>
  <div class="ig-caption">
    <div style="font-size:12px;color:#e9e9ea;line-height:1.5">
      <b style="color:#fff">studio.g85</b> Site novo no ar — feito à mão, do zero.
      Arrasta pra ver as sete páginas, a paleta e o site em três telas. 🏁
    </div>
    <div style="font-size:10px;color:#7a7a80;margin-top:6px;letter-spacing:.04em">HÁ 2 HORAS</div>
  </div>
</div>
<script>{JS}</script>
</body>
</html>"""

outp = HERE / "carrossel-studio-g85.html"
outp.write_text(HTML, encoding="utf-8")
print("OK", outp, f"{outp.stat().st_size/1024/1024:.2f} MB", TOTAL, "slides")
