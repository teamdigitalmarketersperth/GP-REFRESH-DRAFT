"""Shared chrome + helpers for generated pages (imported by make_pages.py and make_tbc.py)."""
import html, json, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTER = "https://events.gprefresh.com/"
e = html.escape

idx = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
HEAD = idx[: idx.index('<link rel="stylesheet" href="assets/css/gpr.css">')]
TICKER = idx[idx.index("<!-- ============ BLOCK: gpr-ticker"): idx.index("<!-- ============ BLOCK: gpr-header")]
HEADER = idx[idx.index("<!-- ============ BLOCK: gpr-header"): idx.index('<main id="top">')]
FOOTER = idx[idx.index("<!-- ============ BLOCK: gpr-footer"): idx.index("<script>")]
def relink(s):
    s = s.replace('href="#top"', 'href="index.html"')
    return re.sub(r'href="#(sydney|brisbane|cruises|dubai|congresses)"', r'href="index.html#\1"', s)
HEADER, FOOTER = relink(HEADER), relink(FOOTER)
SCRIPT = """<script>
[].forEach.call(document.querySelectorAll('[data-rail-nav]'),function(nav){
  var track=document.querySelector('[data-rail="'+nav.getAttribute('data-rail-nav')+'"]'); if(!track) return;
  [].forEach.call(nav.querySelectorAll('[data-dir]'),function(b){b.addEventListener('click',function(){var c=track.firstElementChild;var step=c?c.getBoundingClientRect().width+20:300;track.scrollBy({left:step*+b.getAttribute('data-dir'),behavior:'smooth'})})});
});
[].forEach.call(document.querySelectorAll('.gpr-drawer a'),function(a){a.addEventListener('click',function(){var d=document.querySelector('.gpr-burger');if(d)d.open=false})});
</script>
"""

def page(fname, title, desc, body, extra_head=""):
    head = HEAD.replace("<title>GP Refresh Congress 2027</title>", f"<title>{e(title)}</title>")
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{e(desc)}">', head)
    doc = ("<!doctype html>\n<html lang=\"en-AU\">\n<head>\n" + head + '<link rel="stylesheet" href="assets/css/gpr.css">\n'
           + extra_head + "</head>\n<body>\n" + TICKER + HEADER + '<main id="top" class="gpr-loc">\n' + body + "\n</main>\n" + FOOTER + SCRIPT + "</body>\n</html>\n")
    open(os.path.join(ROOT, fname), "w", encoding="utf-8").write(doc)
    print("wrote", fname, len(doc))

def hero(crumb, eyebrow, h1, lede, metas=(), ctas=()):
    m = "".join(f"<li>{x}</li>" for x in metas)
    c = "".join(ctas)
    return f"""
<section class="gpr-loc-hero gpr-wave gpr-wave--tr gpr-wave--light">
  <div class="gpr-wrap gpr-loc-hero__inner">
    <p class="gpr-crumb"><a href="index.html">Home</a> · More · {e(crumb)}</p>
    <p class="gpr-eyebrow">{eyebrow}</p>
    <h1>{h1}</h1>
    <p class="gpr-lede">{lede}</p>
    {f'<ul class="gpr-loc-meta">{m}</ul>' if m else ''}
    {f'<div class="gpr-loc-hero__ctas">{c}</div>' if c else ''}
  </div>
</section>"""

def rail(name, items, hint="Swipe →"):
    return (f'<div class="gpr-rail"><ul class="gpr-rail__track" data-rail="{name}">{"".join(items)}</ul>'
            f'<p class="gpr-wrap gpr-rail__hint">{hint}</p></div>')

def rail_nav(name):
    return (f'<div class="gpr-rail__nav" data-rail-nav="{name}"><button class="gpr-rail__btn" data-dir="-1" aria-label="Previous">←</button>'
            f'<button class="gpr-rail__btn" data-dir="1" aria-label="Next">→</button></div>')

def pill(href, label, kind="", ext=False):
    t = ' target="_blank" rel="noopener"' if ext else ""
    return f'<a class="gpr-pill{(" gpr-pill--" + kind) if kind else ""}" href="{href}"{t}>{label}</a>'

def register_band(eyebrow, title, lede):
    return f"""
<section class="gpr-section gpr-register">
  <div class="gpr-wrap">
    <p class="gpr-eyebrow">{eyebrow}</p>
    <h2 class="gpr-title">{title}</h2>
    <p class="gpr-lede">{lede}</p>
    <div class="gpr-register__ctas">{pill(REGISTER, "Register now", "ink", True)}{pill("index.html#congresses", "Choose your city")}</div>
  </div>
</section>"""

def person(f, n, t, role=""):
    r = f'<span class="gpr-person__role">{e(role)}</span>' if role else ""
    return (f'<li><article class="gpr-person"><div class="gpr-person__photo"><img src="assets/committee/{f}.jpg" alt="{e(n)}" loading="lazy"></div>'
            f'{r}<h3>{e(n)}</h3><p>{e(t)}</p></article></li>')

