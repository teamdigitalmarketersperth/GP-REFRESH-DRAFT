"""Build an Exhibition location page (exhibition-melbourne.html, ...).
Copy and facts come from the approved 2027 Partnership Prospectus and the 23 Nov exhibitor ads.
Rules: never say "no sponsored talks" here; state that partners can exhibit; CTA "Partner with us".
Run: python3 -I _build/make_exhibition.py melbourne"""
import html, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CITY = sys.argv[1] if len(sys.argv) > 1 else "melbourne"
e = html.escape

CITIES = {
    "melbourne": dict(name="Melbourne", dates="15–16 May 2027", venue="Melbourne Convention and Exhibition Centre (MCEC)",
                      venue_short="MCEC", address="1 Convention Centre Place, South Wharf VIC 3006",
                      venue_img="assets/img/venue-mcec.jpg", line="The 2027 series opens in Australia's cultural capital.",
                      hero="assets/img/hall-01.jpg"),
    "sydney": dict(name="Sydney", dates="26–27 June 2027", venue="International Convention Centre Sydney (ICC Sydney)",
                   venue_short="ICC Sydney", address="14 Darling Drive, Sydney NSW 2000",
                   venue_img="assets/img/venue-icc.jpg", line="The mid-year Congress comes to the harbour city.",
                   hero="assets/img/hall-03.jpg"),
    "brisbane": dict(name="Brisbane", dates="18–19 Sept 2027", venue="Brisbane Convention & Exhibition Centre (BCEC)",
                     venue_short="BCEC", address="Merivale St & Glenelg St, South Brisbane QLD 4101",
                     venue_img="assets/img/venue-bcec.jpg", line="The series closes at the Brisbane Convention and Exhibition Centre.",
                     hero="assets/img/hall-04.jpg"),
}
C = CITIES[CITY]
EMAIL = "connect@gprefresh.com"
HALL = ' class="is-hall"'

idx = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
head = idx[: idx.index('<link rel="stylesheet" href="assets/css/gpr.css">')]
head = head.replace("<title>GP Refresh Congress 2027</title>", f"<title>GP Refresh Exhibition {C['name']}</title>")
head = re.sub(r'<meta name="description" content="[^"]*">',
              f'<meta name="description" content="Exhibit at GP Refresh {e(C["name"])}, {e(C["dates"])} at {e(C["venue_short"])}. Every break is in the Exhibition Hall: 7 breaks and 6 hours face to face with GPs.">', head)
ticker = idx[idx.index("<!-- ============ BLOCK: gpr-ticker"): idx.index("<!-- ============ BLOCK: gpr-header")]
header = idx[idx.index("<!-- ============ BLOCK: gpr-header"): idx.index('<main id="top">')]
footer = idx[idx.index("<!-- ============ BLOCK: gpr-footer"): idx.index("<script>")]
def relink(s):
    s = s.replace('href="#top"', 'href="index.html"')
    return re.sub(r'href="#(sydney|brisbane|cruises|dubai|congresses|gala|speaker-eoi|past|about|advisory|faqs|privacy|terms|exhibition)"',
                  r'href="index.html#\1"', s)
header, footer = relink(header), relink(footer)

DAYS = [("Saturday", [("7:00am", "Registration", 0), ("7:30am", "Breakfast · Exhibition Hall", 1), ("8:40am", "Session 1", 0),
                      ("10:10am", "Morning tea · Exhibition Hall", 1), ("10:50am", "Session 2", 0), ("12:20pm", "Lunch · Exhibition Hall", 1),
                      ("1:50pm", "Session 3", 0), ("3:20pm", "Afternoon tea · Exhibition Hall", 1), ("4:00pm", "Session 4", 0),
                      ("5:00pm", "CPR Workshop", 0), ("7:30pm", "Grand Gala Dinner & Show", 0)]),
        ("Sunday", [("8:40am", "Session 5", 0), ("10:10am", "Morning tea · Exhibition Hall", 1), ("10:40am", "Session 6", 0),
                    ("12:10pm", "Lunch · Exhibition Hall", 1), ("1:30pm", "Session 7", 0), ("3:00pm", "Afternoon tea · Exhibition Hall", 1),
                    ("3:30pm", "Session 8", 0), ("4:30pm", "Congress closes", 0)])]

PACKAGES = [
    ("diamond", "Diamond Partner", "6×9 (54 m²) exhibition booth",
     ["4 exhibitor passes and 6 Gala Dinner tickets", "Acknowledgement at the opening and closing sessions",
      "30-second video ad at the Gala Dinner", "40-minute product launch (online delegates)", "Dedicated social campaign and showcase video",
      "200-word company profile on the partner page"]),
    ("platinum", "Platinum Partner", "6×6 (36 m²) exhibition booth",
     ["2 exhibitor passes and 4 Gala Dinner tickets", "20-minute product launch (online delegates)",
      "Social media spotlight and highlights-video feature", "150-word company profile on the partner page"]),
    ("gold", "Gold Partner", "3×6 (18 m²) exhibition booth",
     ["1 exhibitor pass and 2 Gala Dinner tickets", "Pre-event introduction post and event-day story", "100-word company profile on the partner page"]),
    ("booth", "Exhibition Booth", "3×3 (9 m²) standard booth",
     ["1 exhibitor pass and 1 Gala Dinner pass", "Logo on the GP Refresh partner page", "Non-profit 2×3 (6 m²) booth also available"]),
]
SHARED = "Every package includes tier logo placement on the GP Refresh website, your logo on onsite digital screens, partner board recognition and branded collateral in every delegate satchel."
ROLES = [("Medical representatives", "Your GPs are in the hall, at every break."),
         ("Pharmaceutical and medical device teams", "Your booth sits where every coffee and conversation happens."),
         ("Pharmaceutical industry directors", "One national platform across three cities."),
         ("Practice services and technology", "High-trust conversations with GPs who run their own clinics.")]
GALLERY = [("hall-01", "GPs at breakfast among the booths"), ("hall-02", "Delegates talking over coffee in the Exhibition Hall"),
           ("hall-05", "A busy catering break in the Exhibition Hall"), ("hall-06", "Delegates at lunch in the Exhibition Hall"),
           ("hall-08", "An exhibitor talking with a GP at a booth"), ("hall-09", "GPs visiting an exhibitor booth"),
           ("hall-10", "Exhibitors presenting to a delegate"), ("hall-07", "Delegates in conversation at an exhibitor stand")]

def rail_nav(n):
    return (f'<div class="gpr-rail__nav" data-rail-nav="{n}"><button class="gpr-rail__btn" data-dir="-1" aria-label="Previous">←</button>'
            f'<button class="gpr-rail__btn" data-dir="1" aria-label="Next">→</button></div>')

days = []
for d, rows in DAYS:
    dl = "".join(f'<dt>{t}</dt><dd{HALL if h else ""}>{e(x)}</dd>' for t, x, h in rows)
    days.append(f'<div class="gpr-day"><h3>{"Day 1" if d == "Saturday" else "Day 2"} · {d}</h3><dl>{dl}</dl></div>')
gallery = "".join(f'<li><div class="gpr-photo"><img src="assets/img/{f}.jpg" alt="{e(a)}" loading="lazy"></div></li>' for f, a in GALLERY)
pkgs = "".join(f'<li><article class="gpr-pkg gpr-pkg--{k}"><p class="gpr-pkg__tier">{"Partnership" if k != "booth" else "Booth only"}</p>'
               f'<h3>{e(n)}</h3><p class="gpr-pkg__booth">{e(b)}</p><ul>{"".join(f"<li>{e(x)}</li>" for x in inc)}</ul></article></li>'
               for k, n, b, inc in PACKAGES)
roles = "".join(f"<li><b>{e(a)}</b><span>{e(b)}</span></li>" for a, b in ROLES)

body = f"""<main id="top" class="gpr-loc">

<!-- ============ BLOCK: gpr-loc-hero ============ -->
<section class="gpr-loc-hero gpr-wave gpr-wave--tr gpr-wave--light">
  <div class="gpr-wrap gpr-loc-hero__inner">
    <p class="gpr-crumb"><a href="index.html">Home</a> · Exhibition · {e(C['name'])}</p>
    <p class="gpr-eyebrow">GP Refresh Exhibition · {e(C['name'])} 2027</p>
    <h1>Every break, every conversation, face to face with Australia's GPs.</h1>
    <ul class="gpr-loc-meta">
      <li><b>{e(C['dates'])}</b></li>
      <li>{e(C['venue_short'])}, {e(C['name'])}</li>
      <li>7 Exhibition Hall breaks</li>
    </ul>
    <div class="gpr-loc-hero__ctas">
      <a class="gpr-pill gpr-pill--gold" href="#enquire">Partner with us</a>
      <a class="gpr-pill" href="#packages">See packages</a>
    </div>
  </div>
</section>

<!-- ============ BLOCK: gpr-hall-hero ============ -->
<section class="gpr-hall-hero" aria-label="The GP Refresh Exhibition Hall">
  <img class="gpr-hall-hero__img" src="{C['hero']}" alt="GPs at a catering break among the exhibitor booths">
</section>

<!-- ============ BLOCK: gpr-jump ============ -->
<nav class="gpr-jump" aria-label="On this page">
  <div class="gpr-wrap gpr-jump__row">
    <a href="#agenda">Hall agenda</a><a href="#packages">Packages</a><a href="#national">National Partner</a><a href="#audience">Who exhibits</a><a href="#venue">Venue</a><a href="#enquire">Enquire</a>
  </div>
</nav>

<!-- ============ BLOCK: gpr-facts ============ -->
<section class="gpr-section" style="padding-bottom:0">
  <div class="gpr-wrap">
    <p class="gpr-lede" style="margin-top:0">{e(C['line'])} Partners can exhibit at {e(C['name'])} on its own, or at all three Congresses as an Official National Partner.</p>
    <ul class="gpr-facts" style="margin-top:28px">
      <li><b>7</b><span>breaks in the Exhibition Hall</span></li>
      <li><b>6 hrs</b><span>face to face with GPs</span></li>
      <li><b><small>up to</small>1 in 7</b><span>Australian GPs: our 2027 goal</span></li>
      <li><b>2,300+</b><span>GP registrations in the pre-launch year</span></li>
    </ul>
  </div>
</section>

<!-- ============ BLOCK: gpr-agenda (Exhibition Hall agenda) ============ -->
<section class="gpr-section" id="agenda" aria-labelledby="agenda-title">
  <div class="gpr-wrap gpr-program__grid">
    <div>
      <p class="gpr-eyebrow">The weekend format</p>
      <h2 class="gpr-title" id="agenda-title">Every break is spent in the Exhibition Hall.</h2>
      <p class="gpr-lede">Breakfast, morning tea, lunch and afternoon tea are all served among the booths. More time, more conversations, more opportunities.</p>
      <div class="gpr-photo" style="margin-top:28px"><img src="assets/img/hall-02.jpg" alt="Delegates talking over coffee in the Exhibition Hall" loading="lazy"></div>
    </div>
    <div class="gpr-days">{''.join(days)}</div>
  </div>
</section>

<!-- ============ BLOCK: gpr-gallery ============ -->
<section class="gpr-section" style="padding-top:0" aria-labelledby="gallery-title">
  <div class="gpr-wrap gpr-head">
    <div><p class="gpr-eyebrow">Inside the hall</p><h2 class="gpr-title" id="gallery-title">Where every coffee and conversation happens.</h2></div>
    {rail_nav('gallery')}
  </div>
  <div class="gpr-rail">
    <ul class="gpr-rail__track" data-rail="gallery">{gallery}</ul>
    <p class="gpr-wrap gpr-rail__hint">Swipe →</p>
  </div>
</section>

<!-- ============ BLOCK: gpr-packages ============ -->
<section class="gpr-section gpr-committee" id="packages" aria-labelledby="packages-title">
  <div class="gpr-wrap gpr-head">
    <div>
      <p class="gpr-eyebrow">2027 partnerships now open</p>
      <h2 class="gpr-title" id="packages-title">Diamond. Platinum. Gold.</h2>
      <p class="gpr-lede">Each package is available for one, two or all three Congresses. Book two and save 8%, or all three and save 16%.</p>
    </div>
    {rail_nav('packages')}
  </div>
  <div class="gpr-rail">
    <ul class="gpr-rail__track" data-rail="packages">{pkgs}</ul>
    <p class="gpr-wrap gpr-rail__hint">Swipe for all packages →</p>
  </div>
  <div class="gpr-wrap">
    <p class="gpr-note" style="margin-top:6px">{e(SHARED)}</p>
    <div class="gpr-national" id="national">
      <div>
        <p class="gpr-eyebrow" style="color:var(--gpr-ink)">Official National Partner</p>
        <h3>One partnership. Three cities.</h3>
        <p style="margin:12px 0 0">Exhibit at Melbourne, Sydney and Brisbane to receive National Partner status and save 16%.</p>
      </div>
      <ul>
        <li><b>"Official National Partner of GP Refresh 2027" badge</b>For your website, LinkedIn, email signatures and collateral.</li>
        <li><b>An extra Gala Dinner ticket</b>At every Congress, on top of your package.</li>
        <li><b>Priority booth selection</b>Early access to future booth selection.</li>
      </ul>
    </div>
  </div>
</section>

<!-- ============ BLOCK: gpr-roles ============ -->
<section class="gpr-section gpr-cpd gpr-on-dark gpr-wave gpr-wave--tr" id="audience" aria-labelledby="audience-title">
  <div class="gpr-wrap">
    <div class="gpr-head"><div>
      <p class="gpr-eyebrow">Who exhibits</p>
      <h2 class="gpr-title" id="audience-title">Meet GPs who are inspired, not exhausted.</h2>
      <p class="gpr-lede">Delegates rate GP Refresh 9.7 out of 10. Relationships started in {e(C['name'])} continue across all three cities.</p>
    </div></div>
    <ul class="gpr-roles">{roles}</ul>
  </div>
</section>

<!-- ============ BLOCK: gpr-gala (exhibitor angle) ============ -->
<section class="gpr-section" aria-labelledby="gala-title">
  <div class="gpr-wrap gpr-venue__grid">
    <div class="gpr-venue__img"><img src="assets/img/gala-hall.jpg" alt="The GP Refresh Grand Gala Dinner" loading="lazy"></div>
    <div>
      <p class="gpr-eyebrow">Saturday night</p>
      <h2 class="gpr-title" id="gala-title">The conversation continues at the Gala Dinner.</h2>
      <p class="gpr-lede">Every partnership package includes complimentary Grand Gala Dinner tickets.</p>
    </div>
  </div>
</section>

<!-- ============ BLOCK: gpr-venue ============ -->
<section class="gpr-section gpr-venue gpr-committee" id="venue" aria-labelledby="venue-title">
  <div class="gpr-wrap gpr-venue__grid">
    <div class="gpr-venue__img"><img src="{C['venue_img']}" alt="{e(C['venue'])}" loading="lazy"></div>
    <div>
      <p class="gpr-eyebrow">Venue</p>
      <h2 class="gpr-title" id="venue-title">{e(C['venue'])}</h2>
      <dl>
        <div><dt>Dates</dt><dd>{e(C['dates'])}</dd></div>
        <div><dt>Address</dt><dd>{e(C['address'])}</dd></div>
        <div><dt>Exhibition Hall</dt><dd>Open for every catering break, both days</dd></div>
      </dl>
    </div>
  </div>
</section>

<!-- ============ BLOCK: gpr-enquire ============ -->
<section class="gpr-section" id="enquire" aria-labelledby="enquire-title">
  <div class="gpr-wrap">
    <p class="gpr-eyebrow">Partner with us</p>
    <h2 class="gpr-title" id="enquire-title">Request the 2027 Partnership Prospectus.</h2>
    <p class="gpr-lede">Pricing, booth plans and package details for {e(C['name'])}, Sydney and Brisbane are in the prospectus. Contact the partnerships team and we'll send it to you.</p>
    <ul class="gpr-enquire">
      <li><small>Email</small><b>{EMAIL}</b></li>
      <li><small>Phone</small><b>1300 477 337</b></li>
      <li><small>Ask for</small><b>2027 Partnership Prospectus · {e(C['name'])}</b></li>
    </ul>
  </div>
</section>

</main>
"""

script = """<script>
[].forEach.call(document.querySelectorAll('[data-rail-nav]'),function(nav){
  var track=document.querySelector('[data-rail="'+nav.getAttribute('data-rail-nav')+'"]'); if(!track) return;
  [].forEach.call(nav.querySelectorAll('[data-dir]'),function(b){b.addEventListener('click',function(){var c=track.firstElementChild;var step=c?c.getBoundingClientRect().width+20:300;track.scrollBy({left:step*+b.getAttribute('data-dir'),behavior:'smooth'})})});
});
[].forEach.call(document.querySelectorAll('.gpr-drawer a'),function(a){a.addEventListener('click',function(){var d=document.querySelector('.gpr-burger');if(d)d.open=false})});
</script>
"""
doc = ("<!doctype html>\n<html lang=\"en-AU\">\n<head>\n" + head + '<link rel="stylesheet" href="assets/css/gpr.css">\n</head>\n<body>\n'
       + ticker + header + body + footer + script + "</body>\n</html>\n")
dst = os.path.join(ROOT, f"exhibition-{CITY}.html")
open(dst, "w", encoding="utf-8").write(doc)
print("wrote", dst, len(doc))
