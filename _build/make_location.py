"""Build a Congress location page (melbourne.html, sydney.html, ...) from index.html's
header/footer plus shared data. Run: python3 -I _build/make_location.py melbourne"""
import html, json, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CITY = sys.argv[1] if len(sys.argv) > 1 else "melbourne"

CITIES = {
    "melbourne": dict(name="Melbourne", dates="15–16 May 2027", start="2027-05-15T08:00:00+10:00",
                      venue="Melbourne Convention and Exhibition Centre (MCEC)", venue_short="MCEC",
                      address="1 Convention Centre Place, South Wharf VIC 3006",
                      venue_img="assets/img/venue-mcec.jpg", city_img="assets/img/city-melbourne.jpg",
                      film="assets/video/melbourne-2026.mp4", film_poster="assets/video/melbourne-2026.jpg",
                      film_label="GP Refresh Melbourne 2026", youtube=None),
    "sydney": dict(name="Sydney", dates="26–27 June 2027", start="2027-06-26T08:00:00+10:00",
                   venue="International Convention Centre Sydney (ICC Sydney)", venue_short="ICC Sydney",
                   address="14 Darling Drive, Sydney NSW 2000",
                   venue_img="assets/img/venue-icc.jpg", city_img="assets/img/city-sydney.jpg",
                   film=None, film_poster=None, film_label="GP Refresh Sydney 2026 highlights", youtube="NiG_xOsDrd8"),
    "brisbane": dict(name="Brisbane", dates="18–19 Sept 2027", start="2027-09-18T08:00:00+10:00",
                     venue="Brisbane Convention & Exhibition Centre (BCEC)", venue_short="BCEC",
                     address="Merivale St & Glenelg St, South Brisbane QLD 4101",
                     venue_img="assets/img/venue-bcec.jpg", city_img="assets/img/city-brisbane.jpg",
                     film=None, film_poster=None, film_label="GP Refresh Brisbane 2026 highlights", youtube="LV4rYFZLOHo"),
}
C = CITIES[CITY]
REGISTER = "https://events.gprefresh.com/"
HALL = ' class="is-hall"'
MORE = ' class="gpr-speakers__more" hidden'
e = html.escape

# ---- shared chrome from the homepage ----
idx = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
head = idx[: idx.index('<link rel="stylesheet" href="assets/css/gpr.css">')]
head = head.replace("<title>GP Refresh Congress 2027</title>",
                    f"<title>GP Refresh {C['name']} 2027</title>")
head = re.sub(r'<meta name="description" content="[^"]*">',
              f'<meta name="description" content="GP Refresh Congress {e(C["name"])}, {e(C["dates"])} at {e(C["venue_short"])}. 70+ clinical topics in 6-minute talks, up to 53 CPD hours, group discounts up to 65% off.">', head)
ticker = idx[idx.index("<!-- ============ BLOCK: gpr-ticker"): idx.index("<!-- ============ BLOCK: gpr-header")]
header = idx[idx.index("<!-- ============ BLOCK: gpr-header"): idx.index('<main id="top">')]
footer = idx[idx.index("<!-- ============ BLOCK: gpr-footer"): idx.index("<script>")]
def relink(s):
    s = s.replace('href="#top"', 'href="index.html"')
    return re.sub(r'href="#(sydney|brisbane|cruises|dubai|congresses|gala|speaker-eoi|past|about|advisory|faqs|privacy|terms|exhibition)"',
                  r'href="index.html#\1"', s)
header, footer = relink(header), relink(footer)

# ---- data ----
program = json.load(open(os.path.join(ROOT, "_source", "program.json"), encoding="utf-8"))
n_topics = sum(len(s["topics"]) for s in program)
SPEAKERS = [l for l in """Dr Justin Coleman|Specialist GP
Dr Nicole Higgins|Past RACGP President
Dr Bruce Willett|Past RACGP Vice-President
Dr Catherine Eltringham|Specialist GP
Dr Ian Kamerman|Specialist GP
Dr Prakash Appanna|Haematologist
Dr Jonathan Banks|Respiratory Physician
Dr Art Kaminski|Radiation Oncologist
Dr Sarah Kentwell|Respiratory Physician
Dr Richard Turner|Respiratory Physician
Dr Karthik Gopal|Cardiologist
Dr Belinda Glasson|Specialist GP
Dr Akshay Mishra|Cardiologist
Dr Maryam Bayat|Cardiologist
Dr Prath Nakka|Breast and Endocrine Surgeon
Dr Pradeep K Ramaswamy|Gastroenterologist
Dr Shunil Sharma|Rheumatologist
Dr Samantha Peden|Vascular Surgeon
Dr Michael Reid|Orthopaedic Surgeon
Dr Mathew Hope|Orthopaedic Surgeon
Dr Shailendhra Bethi|Psychiatrist
Dr Laurence Kemp|Academic GP
Dr Rohit Bansal|Geriatrician
Dr Viral Upadhyay|Neurologist
Dr Ramesh Damodaran|General Surgeon
Dr Caroline Hardy|Specialist GP
Dr Krystyna De Lange|Psychologist
Dr Soheil Farnagi|Gynaecologist
Dr Dakshinamurthy Divi|Nephrologist
Dr Rajeev Jarugula|Emergency Physician
Dr Naveen Somia|Plastic Surgeon
Dr Katherine Wyld|Endocrinologist
Dr Brandon Cadd|ENT Surgeon
Dr Casey Going|Specialist GP
Dr Natasha Yates|Specialist GP
Dr Benny Yau|Dermatologist
Dr Hillary Brown|Dermatologist
Dr Ravi Tankala|Paediatrician
Dr Lina Chen|Gastroenterologist
Dr Alex Newman|Ophthalmologist
Dr Randeep Bindra|Orthopaedic Surgeon
Dr Anthony Khoo|Dietitian
Dr Paris Dale|Movember
Dr Solomon Shatananda|Child and Adolescent Psychiatrist""".splitlines()]
DAYS = [("Saturday", [("7:00am", "Registration", 0), ("7:30am", "Breakfast · Exhibition Hall", 1), ("8:30am", "Congress opens", 0),
                      ("8:40am", "Session 1 · talks + panel", 0), ("10:10am", "Morning tea · Exhibition Hall", 1),
                      ("10:50am", "Session 2 · talks + panel", 0), ("12:20pm", "Lunch · Exhibition Hall", 1),
                      ("1:50pm", "Session 3 · talks + panel", 0), ("3:20pm", "Afternoon tea · Exhibition Hall", 1),
                      ("4:00pm", "Session 4 · talks + panel", 0), ("5:00pm", "CPR Workshop", 0),
                      ("7:00pm", "Gala pre-drinks", 0), ("7:30pm", "Grand Gala Dinner & Show", 0)]),
        ("Sunday", [("8:30am", "Congress re-opens", 0), ("8:40am", "Session 5 · talks + panel", 0), ("10:10am", "Morning tea · Exhibition Hall", 1),
                    ("10:40am", "Session 6 · talks + panel", 0), ("12:10pm", "Lunch · Exhibition Hall", 1),
                    ("1:30pm", "Session 7 · talks + panel", 0), ("3:00pm", "Afternoon tea · Exhibition Hall", 1),
                    ("3:30pm", "Session 8 · talks + panel", 0), ("4:30pm", "Congress closes", 0)])]
CPD = [("Pre-Congress activity", 12, 6, 1), ("Congress Day 1", 6, 0, 0), ("Congress Day 2", 6, 0, 0),
       ("CPR Workshop", 2, 0, 0), ("Post-Congress activity", 4, 8, 8)]
FULL = 1499
TIERS = [("2+ GPs", 52), ("5+ GPs", 55), ("10+ GPs", 60), ("15+ GPs", 65)]
COMMITTEE = [("dr-justin", "Dr Justin Coleman", "Editor, Murtagh's General Practice 9th Ed.", "Chair"),
             ("dr-nicole", "Dr Nicole Higgins", "Past RACGP President", "Member"),
             ("dr-bruce", "Dr Bruce Willett", "Past RACGP Vice-President", "Member"),
             ("dr-catherine", "Dr Catherine Eltringham", "Specialist GP", "Member"),
             ("dr-ian", "Dr Ian Kamerman", "Specialist GP", "Member")]

def money(v):
    s = f"{v:,.2f}"
    return "$" + (s[:-3] if s.endswith(".00") else s)

def rail_nav(name):
    return (f'<div class="gpr-rail__nav" data-rail-nav="{name}"><button class="gpr-rail__btn" data-dir="-1" aria-label="Previous">←</button>'
            f'<button class="gpr-rail__btn" data-dir="1" aria-label="Next">→</button></div>')

# ---- sections ----
out = []
out.append(f"""<main id="top" class="gpr-loc">

<!-- ============ BLOCK: gpr-loc-hero ============ -->
<section class="gpr-loc-hero gpr-wave gpr-wave--tr gpr-wave--light">
  <div class="gpr-wrap gpr-loc-hero__inner">
    <p class="gpr-crumb"><a href="index.html">Home</a> · Congress · {e(C['name'])}</p>
    <p class="gpr-eyebrow">GP Refresh Congress {e(C['name'])} 2027</p>
    <h1>Join the 6-Minute GP Refresh CPD Revolution</h1>
    <ul class="gpr-loc-meta">
      <li><b>{e(C['dates'])}</b></li>
      <li>{e(C['venue_short'])}, {e(C['name'])}</li>
      <li>Up to 53 CPD hours</li>
    </ul>
    <div class="gpr-loc-hero__ctas">
      <a class="gpr-pill gpr-pill--gold" href="{REGISTER}" target="_blank" rel="noopener">Register for {e(C['name'])}</a>
      <a class="gpr-pill" href="#pricing">Group pricing</a>
    </div>
  </div>
</section>
""")
if C["film"]:
    film = (f'<video src="{C["film"]}" poster="{C["film_poster"]}" controls playsinline preload="none" '
            f'aria-label="{e(C["film_label"])}"></video>')
    film_link = '<a href="https://www.youtube.com/@GPRefreshConference" target="_blank" rel="noopener">More on YouTube ↗</a>'
else:
    yt = C["youtube"]
    film = (f'<a href="https://www.youtube.com/watch?v={yt}" target="_blank" rel="noopener" class="gpr-clip" style="height:100%">'
            f'<div class="gpr-clip__thumb" style="height:100%;border:0;border-radius:0"><img src="assets/testimonials/{yt}.jpg" alt="" loading="lazy">'
            f'<span class="gpr-clip__play">Watch on YouTube</span></div></a>')
    film_link = f'<a href="https://www.youtube.com/watch?v={yt}" target="_blank" rel="noopener">Watch on YouTube ↗</a>'
out.append(f"""
<!-- ============ BLOCK: gpr-loc-film (last year's Congress in this city) ============ -->
<section class="gpr-loc-film" aria-label="{e(C['film_label'])}">
  <div class="gpr-wrap">
    <div class="gpr-loc-film__frame">{film}</div>
    <p class="gpr-loc-film__cap"><span>{e(C['film_label'])}</span>{film_link}</p>
  </div>
</section>

<!-- ============ BLOCK: gpr-jump ============ -->
<nav class="gpr-jump" aria-label="On this page">
  <div class="gpr-wrap gpr-jump__row">
    <a href="#topics">Clinical topics</a><a href="#cpd">CPD hours</a><a href="#pricing">Pricing</a><a href="#speakers">Speakers</a><a href="#committee">Scientific Committee</a><a href="#venue">Venue</a>
  </div>
</nav>

<!-- ============ BLOCK: gpr-intro (what 6 minutes means) ============ -->
<section class="gpr-section" style="padding-bottom:0">
  <div class="gpr-wrap">
    <div class="gpr-intro__shift" aria-label="One-hour lecture becomes a six-minute talk"><s>1-hour lecture</s><i aria-hidden="true"></i><b>6-minute talk</b></div>
    <p class="gpr-lede" style="margin-top:0">Leading clinicians distil a 1-hour lecture into a 6-minute TED-style talk, each with a clear learning outcome. Two days, eight sessions, panel discussions after each block, and every break in the Exhibition Hall.</p>
    <ul class="gpr-facts" style="margin-top:32px">
      <li><b>70+</b><span>clinical topics and learning outcomes</span></li>
      <li><b><small>up to</small>53</b><span>CPD hours</span></li>
      <li><b>8</b><span>sessions over two days</span></li>
      <li><b>7</b><span>breaks in the Exhibition Hall</span></li>
    </ul>
  </div>
</section>
""")

# Clinical topics
sess = []
for s in program:
    items = "".join(f'<li><b>{e(t["topic"])}</b><span>{e(t["talk"])}</span></li>' for t in s["topics"])
    note = f' · {e(s["note"])}' if s.get("note") else ""
    sess.append(f'<details class="gpr-session"{" open" if s["n"] == 1 else ""}><summary>'
                f'<span class="gpr-session__n">{s["n"]}</span><span class="gpr-session__title">{e(s["title"])}</span>'
                f'<span class="gpr-session__when">Session {s["n"]} · {e(s["day"])}{note}</span>'
                f'<span class="gpr-session__count">{len(s["topics"])} topics</span></summary><ol>{items}</ol></details>')
days = []
for d, rows in DAYS:
    dl = "".join(f'<dt>{t}</dt><dd{HALL if hall else ""}>{e(x)}</dd>' for t, x, hall in rows)
    days.append(f'<div class="gpr-day"><h3>{"Day 1" if d == "Saturday" else "Day 2"} · {d}</h3><dl>{dl}</dl></div>')
out.append(f"""
<!-- ============ BLOCK: gpr-program (clinical topics + weekend format) ============ -->
<section class="gpr-section" id="topics" aria-labelledby="topics-title">
  <div class="gpr-wrap">
    <div class="gpr-head"><div>
      <p class="gpr-eyebrow">Program</p>
      <h2 class="gpr-title" id="topics-title">70+ clinical topics.</h2>
      <p class="gpr-lede">Every topic is a 6-minute talk with a clear learning outcome. Open a session to see its topics.</p>
      <p class="gpr-note">Shown: the {n_topics} topics from the 2026 program. The {e(C['name'])} 2027 program is announced soon.</p>
    </div></div>
    <div class="gpr-program__grid">
      <div>{''.join(sess)}</div>
      <div class="gpr-days">{''.join(days)}</div>
    </div>
  </div>
</section>
""")

# CPD
rows = "".join(f"<tr><td>{e(a)}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{b+c+d}</td></tr>" for a, b, c, d in CPD)
tot = [sum(r[i] for r in CPD) for i in (1, 2, 3)]
out.append(f"""
<!-- ============ BLOCK: gpr-cpd-table ============ -->
<section class="gpr-section gpr-cpd gpr-on-dark gpr-wave gpr-wave--tr" id="cpd" aria-labelledby="cpd-title">
  <div class="gpr-wrap">
    <div class="gpr-head"><div>
      <p class="gpr-eyebrow">CPD hours allocation</p>
      <p class="gpr-cpd__big"><small>up to</small>{sum(tot)}</p>
      <h2 class="gpr-title" id="cpd-title">CPD hours, recognised by your college.</h2>
    </div></div>
    <div class="gpr-table-wrap">
      <table class="gpr-table">
        <thead><tr><th>Activity</th><th>Educational activities</th><th>Reviewing performance</th><th>Measuring outcomes</th><th>Total</th></tr></thead>
        <tbody>{rows}</tbody>
        <tfoot><tr><td>Total</td><td>{tot[0]}</td><td>{tot[1]}</td><td>{tot[2]}</td><td>{sum(tot)}</td></tr></tfoot>
      </table>
    </div>
    <div class="gpr-cpd__logos">
      <span><img src="assets/cpd/racgp.jpg" alt="RACGP CPD Accredited Activity" loading="lazy"></span>
      <span><img src="assets/cpd/acrrm.png" alt="ACRRM CPD" loading="lazy"></span>
      <span><img src="assets/cpd/rnzcgp.png" alt="RNZCGP, up to 80 CME credits" loading="lazy"></span>
    </div>
    <p class="gpr-lede" style="font-size:15px">RNZCGP members can claim up to 80 CME credits.</p>
  </div>
</section>
""")

# Pricing
tiers = []
for i, (label, off) in enumerate(TIERS):
    price = round(FULL * (100 - off) / 100, 2)
    best = " gpr-tier--best" if i == len(TIERS) - 1 else ""
    tiers.append(f'<article class="gpr-tier{best}"><p class="gpr-tier__label">{label}</p>'
                 f'<p class="gpr-tier__off">{off}%<small>off</small></p>'
                 f'<p class="gpr-tier__price">{money(price)}<s>{money(FULL)}</s><span class="gpr-tier__unit">per Congress Pass</span></p></article>')
out.append(f"""
<!-- ============ BLOCK: gpr-price ============ -->
<section class="gpr-section gpr-price gpr-on-dark gpr-wave gpr-wave--bl" id="pricing" aria-labelledby="price-title" style="border-top:1px solid rgba(236,236,234,.12)">
  <div class="gpr-wrap">
    <div class="gpr-head"><div>
      <p class="gpr-eyebrow">Group discounts · end 30 December</p>
      <h2 class="gpr-title" id="price-title">Book with a colleague. You both save 52%.</h2>
      <p class="gpr-lede">Bring more GPs and save more, up to 65% off every Congress Pass.</p>
    </div></div>
    <div class="gpr-tiers">{''.join(tiers)}</div>
    <ul class="gpr-price__incl">
      <li><b>Congress Pass · {money(FULL)}</b>Full program and materials, lunch and coffee breaks.</li>
      <li><b>Grand Gala Dinner · included</b>Valued at $329, Saturday night.</li>
      <li><b>CPR Workshop · included</b>Valued at $100, for every delegate.</li>
    </ul>
    <p class="gpr-price__note">Prices per person in Australian dollars, including GST. See the terms and conditions.</p>
    <div class="gpr-price__ctas">
      <a class="gpr-pill gpr-pill--gold" href="{REGISTER}" target="_blank" rel="noopener">Book your group</a>
      <a class="gpr-pill" href="{REGISTER}" target="_blank" rel="noopener">Register individually</a>
    </div>
  </div>
</section>
""")

# Speakers
FIRST = 12
cards = "".join(f'<li{MORE if i >= FIRST else ""}><b>{e(n)}</b><span>{e(r)}</span></li>'
                for i, (n, r) in enumerate(l.split("|") for l in SPEAKERS))
out.append(f"""
<!-- ============ BLOCK: gpr-speakers ============ -->
<section class="gpr-section" id="speakers" aria-labelledby="speakers-title">
  <div class="gpr-wrap">
    <div class="gpr-head"><div>
      <p class="gpr-eyebrow">Speakers &amp; panellists</p>
      <h2 class="gpr-title" id="speakers-title">Leading clinicians, 6 minutes each.</h2>
      <p class="gpr-note">Shown: the 2026 faculty of {len(SPEAKERS)}. {e(C['name'])} 2027 speakers are announced soon.</p>
    </div></div>
    <ul class="gpr-speakers__grid">{cards}</ul>
    <button class="gpr-pill gpr-speakers__toggle" type="button" data-more>Show all {len(SPEAKERS)} speakers</button>
  </div>
</section>
""")

# Committee
people = "".join(f'<li><article class="gpr-person"><div class="gpr-person__photo"><img src="assets/committee/{f}.jpg" alt="{e(n)}" loading="lazy"></div>'
                 f'<span class="gpr-person__role">{r}</span><h3>{e(n)}</h3><p>{e(t)}</p></article></li>' for f, n, t, r in COMMITTEE)
out.append(f"""
<!-- ============ BLOCK: gpr-committee ============ -->
<section class="gpr-section gpr-committee" id="committee" aria-labelledby="committee-title">
  <div class="gpr-wrap gpr-head">
    <div><p class="gpr-eyebrow">Scientific Committee</p><h2 class="gpr-title" id="committee-title">Meet the GP Refresh Scientific Committee.</h2></div>
    {rail_nav('committee')}
  </div>
  <div class="gpr-rail">
    <ul class="gpr-rail__track" data-rail="committee">{people}</ul>
    <p class="gpr-wrap gpr-rail__hint">Swipe →</p>
  </div>
</section>

<!-- ============ BLOCK: gpr-venue ============ -->
<section class="gpr-section gpr-venue" id="venue" aria-labelledby="venue-title">
  <div class="gpr-wrap gpr-venue__grid">
    <div class="gpr-venue__img"><img src="{C['venue_img']}" alt="{e(C['venue'])}" loading="lazy"></div>
    <div>
      <p class="gpr-eyebrow">Venue</p>
      <h2 class="gpr-title" id="venue-title">{e(C['venue'])}</h2>
      <dl>
        <div><dt>Dates</dt><dd>{e(C['dates'])}</dd></div>
        <div><dt>Address</dt><dd>{e(C['address'])}</dd></div>
        <div><dt>Saturday night</dt><dd>Grand Gala Dinner &amp; Show</dd></div>
      </dl>
      <p style="margin-top:24px"><a class="gpr-pill" href="https://www.google.com/maps/search/?api=1&amp;query={e(C['venue'].replace(' ', '+'))}" target="_blank" rel="noopener">Open in Maps</a></p>
    </div>
  </div>
</section>

<!-- ============ BLOCK: gpr-register ============ -->
<section class="gpr-section gpr-register">
  <div class="gpr-wrap">
    <p class="gpr-eyebrow">{e(C['name'])} · {e(C['dates'])}</p>
    <h2 class="gpr-title">Secure your place in {e(C['name'])}.</h2>
    <p class="gpr-lede">Group discounts of up to 65% end 30 December.</p>
    <div class="gpr-register__ctas">
      <a class="gpr-pill gpr-pill--ink" href="{REGISTER}" target="_blank" rel="noopener">Register now</a>
      <a class="gpr-pill" href="index.html#congresses">Other Congresses</a>
    </div>
  </div>
</section>

</main>
""")

script = """<script>
[].forEach.call(document.querySelectorAll('[data-rail-nav]'),function(nav){
  var track=document.querySelector('[data-rail="'+nav.getAttribute('data-rail-nav')+'"]'); if(!track) return;
  [].forEach.call(nav.querySelectorAll('[data-dir]'),function(b){b.addEventListener('click',function(){var c=track.firstElementChild;var step=c?c.getBoundingClientRect().width+20:300;track.scrollBy({left:step*+b.getAttribute('data-dir'),behavior:'smooth'})})});
});
var more=document.querySelector('[data-more]');
if(more){more.addEventListener('click',function(){var hidden=document.querySelectorAll('.gpr-speakers__more[hidden]');
  if(hidden.length){[].forEach.call(hidden,function(li){li.hidden=false});more.textContent='Show fewer speakers';}
  else{[].forEach.call(document.querySelectorAll('.gpr-speakers__more'),function(li){li.hidden=true});more.textContent=more.textContent.replace('Show fewer speakers','Show all speakers');document.getElementById('speakers').scrollIntoView();}
});}
[].forEach.call(document.querySelectorAll('.gpr-drawer a'),function(a){a.addEventListener('click',function(){var d=document.querySelector('.gpr-burger');if(d)d.open=false})});
</script>
"""

doc = ("<!doctype html>\n<html lang=\"en-AU\">\n<head>\n" + head.replace('<meta charset="utf-8">\n', '') .replace("<title>", '<meta charset="utf-8">\n<title>', 1)
       + '<link rel="stylesheet" href="assets/css/gpr.css">\n</head>\n<body>\n'
       + ticker + header + "".join(out) + footer + script + "</body>\n</html>\n")
dst = os.path.join(ROOT, f"{CITY}.html")
open(dst, "w", encoding="utf-8").write(doc)
print("wrote", dst, len(doc), "bytes;", n_topics, "topics;", len(SPEAKERS), "speakers")
