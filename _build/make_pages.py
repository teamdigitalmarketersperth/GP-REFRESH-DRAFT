"""Build the More-menu pages. Run: python3 -I _build/make_pages.py"""
import html, json, os, importlib.util
e = html.escape
_spec = importlib.util.spec_from_file_location("lib", os.path.join(os.path.dirname(os.path.abspath(__file__)), "make_pages_lib.py"))
lib = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(lib)
ROOT, REGISTER = lib.ROOT, lib.REGISTER
page, hero, rail, rail_nav, pill, register_band, person = lib.page, lib.hero, lib.rail, lib.rail_nav, lib.pill, lib.register_band, lib.person

# ============================ Gala Dinner ============================
gallery = [("gala-show", "Performers on stage at the Gala Dinner show"), ("gala-02", "A delegate dancing at the Gala Dinner"),
           ("gala-01", "A performer on the Gala Dinner dance floor"), ("gala-04", "Guests talking over drinks"),
           ("gala-03", "Wine glasses set for the Gala Dinner")]
cities = [("Melbourne", "Saturday 15 May 2027"), ("Sydney", "Saturday 26 June 2027"), ("Brisbane", "Saturday 18 Sept 2027")]
page("gala-dinner.html", "GP Refresh Gala Dinner", "The GP Refresh Grand Gala Dinner & Show: fine dining, live performances and a night with fellow GPs. Included with every Congress Pass.",
     hero("Gala Dinner", "Saturday night · every Congress", "Let's celebrate General Practice.",
          "The GP Refresh Grand Gala Dinner. This is not just dinner. It's a Grand Show.",
          ["<b>7:00pm pre-drinks</b>", "7:30pm–10:30pm dinner &amp; show", "Dress code: formal"],
          [pill(REGISTER, "Register now", "gold", True), pill("#tickets", "Tickets")]) + f"""
<section class="gpr-hall-hero" aria-label="The Gala Dinner hall"><img class="gpr-hall-hero__img" src="assets/img/gala-hall.jpg" alt="The GP Refresh Grand Gala Dinner hall, set for the evening"></section>

<section class="gpr-section">
  <div class="gpr-wrap gpr-prose">
    <p class="gpr-eyebrow">The experience</p>
    <h2 class="gpr-title">Connections like never before.</h2>
    <p class="gpr-lede">Step into a night where sophistication meets surprise. An exquisite menu of fine food and wine, and a series of live performances designed to delight, from the first sip to the final encore.</p>
  </div>
</section>

<section class="gpr-section" style="padding-top:0" aria-labelledby="gala-gallery">
  <div class="gpr-wrap gpr-head"><div><p class="gpr-eyebrow">Gallery</p><h2 class="gpr-title" id="gala-gallery">From past Gala Dinners.</h2></div>{rail_nav('gala')}</div>
  {rail('gala', [f'<li><div class="gpr-photo"><img src="assets/img/{f}.jpg" alt="{e(a)}" loading="lazy"></div></li>' for f, a in gallery])}
</section>

<section class="gpr-section gpr-cpd gpr-on-dark gpr-wave gpr-wave--bl" id="tickets" aria-labelledby="tickets-title">
  <div class="gpr-wrap">
    <div class="gpr-head"><div>
      <p class="gpr-eyebrow">Tickets</p>
      <h2 class="gpr-title" id="tickets-title">Included with every Congress Pass.</h2>
      <p class="gpr-lede">The Grand Gala Dinner (valued at $329) is complimentary for every delegate. Additional guest tickets can be added during registration. Places are limited.</p>
    </div></div>
    <ul class="gpr-grid">{"".join(f'<li class="gpr-card gpr-card--dark"><h3>{c}</h3><ul><li><b>Date</b>{d}</li><li><b>Time</b>7:00pm pre-drinks · 7:30pm dinner &amp; show</li><li><b>Venue</b>Announced soon</li></ul></li>' for c, d in cities)}</ul>
    <div class="gpr-price__ctas">{pill(REGISTER, "Register and book tickets", "gold", True)}</div>
  </div>
</section>
""" + register_band("Group discounts end 30 December", "Book with a colleague. You both save 52%.", "Every Congress Pass includes the Grand Gala Dinner and the CPR Workshop."))

# ============================ Speaker EOI ============================
program = json.load(open(os.path.join(ROOT, "_source", "program.json"), encoding="utf-8"))
areas = "".join(f'<li class="gpr-card"><p class="gpr-eyebrow" style="font-size:11px">Session {s["n"]}</p><h3 style="font-size:22px;margin-top:8px">{e(s["title"])}</h3></li>' for s in program)
page("speaker-eoi.html", "Speak at GP Refresh", "Expression of interest for speakers at GP Refresh Congress 2027: deliver a 6-minute TED-style talk to Australian GPs in Melbourne, Sydney or Brisbane.",
     hero("Speaker EOI", "Speaker expression of interest · 2027", "Teach what GPs need to know, in 6 minutes.",
          "GP Refresh invites specialists and specialist GPs to distil a 1-hour lecture into one focused 6-minute TED-style talk, followed by a 30-minute panel discussion.",
          ["Melbourne · Sydney · Brisbane", "6-minute talks", "30-min panels"],
          [pill("#apply", "Express interest", "gold")]) + f"""
<section class="gpr-section">
  <div class="gpr-wrap gpr-program__grid">
    <div>
      <p class="gpr-eyebrow">The format</p>
      <h2 class="gpr-title">One topic. One learning outcome. Six minutes.</h2>
      <p class="gpr-lede">Every talk covers the essentials of a common GP presentation: what to look for, what to do, and what has changed. Delegates send questions through the GP Refresh app, and the panel answers them after each block of talks.</p>
    </div>
    <ol class="gpr-steps">
      <li><div><b>6-minute TED-style talk</b><span>Practical, evidence-based and sponsor-free.</span></div></li>
      <li><div><b>30-minute panel discussion</b><span>Answer delegate questions with fellow speakers.</span></div></li>
      <li><div><b>Reviewed by the Scientific Committee</b><span>Chaired by Dr Justin Coleman, Editor of Murtagh's General Practice.</span></div></li>
    </ol>
  </div>
</section>

<section class="gpr-section gpr-committee" aria-labelledby="areas-title">
  <div class="gpr-wrap">
    <div class="gpr-head"><div><p class="gpr-eyebrow">Session areas</p><h2 class="gpr-title" id="areas-title">Where your talk could fit.</h2>
    <p class="gpr-lede">Based on the 2026 program. 2027 session areas may change.</p></div></div>
    <ul class="gpr-grid gpr-grid--4">{areas}</ul>
  </div>
</section>

<section class="gpr-section" id="apply" aria-labelledby="apply-title">
  <div class="gpr-wrap">
    <p class="gpr-eyebrow">Express interest</p>
    <h2 class="gpr-title" id="apply-title">Tell us what you'd like to teach.</h2>
    <p class="gpr-lede">Email the CPD, Delegate &amp; Speaker team with your name, specialty, proposed topic and preferred city.</p>
    <ul class="gpr-enquire">
      <li><small>Email</small><b>cpd@gprefresh.com</b></li>
      <li><small>Contact</small><b>Amal Bose, CPD, Delegate &amp; Speaker Manager</b></li>
      <li><small>Phone</small><b>1300 477 337</b></li>
    </ul>
  </div>
</section>
""")

# ============================ Past Congresses ============================
PAST = [
    ("Brisbane", "12–13 September 2026", "Brisbane", ("yt", "LV4rYFZLOHo"), ["past-bne-1", "past-bne-2", "past-bne-3", "past-bne-4"]),
    ("Melbourne", "15–16 August 2026", "Melbourne", ("mp4", "melbourne-2026"), []),
    ("Sydney", "19–21 June 2026", "Sydney", ("yt", "NiG_xOsDrd8"), ["past-syd-1", "past-syd-2", "past-syd-3", "gala-05"]),
    ("Gold Coast", "1–2 November 2025", "The Langham, Gold Coast", ("yt", "lchxiPuE_tw"), []),
]
blocks = []
for name, dates, where, (kind, ref), photos in PAST:
    if kind == "yt":
        media = (f'<a class="gpr-clip" href="https://www.youtube.com/watch?v={ref}" target="_blank" rel="noopener" style="height:100%">'
                 f'<div class="gpr-clip__thumb" style="height:100%;border:0;border-radius:0"><img src="assets/testimonials/{ref}.jpg" alt="" loading="lazy">'
                 f'<span class="gpr-clip__play">Watch highlights</span></div></a>')
    else:
        media = f'<video src="assets/video/{ref}.mp4" poster="assets/video/{ref}.jpg" controls playsinline preload="none" aria-label="GP Refresh {name} 2026"></video>'
    side = ""
    if photos:
        side = '<div class="gpr-past__thumbs">' + "".join(f'<div><img src="assets/img/{p}.jpg" alt="GP Refresh {name} {dates[-4:]}" loading="lazy"></div>' for p in photos) + "</div>"
    elif name == "Gold Coast":
        side = (f'<a class="gpr-clip" href="https://www.youtube.com/watch?v=OsW1mSVQNYE" target="_blank" rel="noopener"><div class="gpr-clip__thumb">'
                f'<img src="assets/testimonials/OsW1mSVQNYE.jpg" alt="" loading="lazy"><span class="gpr-clip__play">Watch</span></div>'
                f'<h3 style="color:var(--gpr-ink)">GP Refresh 2025 at The Langham Gold Coast</h3></a>')
    blocks.append(f"""<article class="gpr-past"><div class="gpr-past__head"><h2>{e(name)} {dates[-4:]}</h2><p>{e(dates)} · {e(where)}</p></div>
      <div class="gpr-past__grid"><div class="gpr-past__media">{media}</div>{side}</div></article>""")
page("past-congresses.html", "GP Refresh Past Congresses", "Highlights, films and photos from past GP Refresh Congresses in Brisbane, Melbourne, Sydney and the Gold Coast.",
     hero("Past Congresses", "GP Refresh highlights", "Past Congresses.",
          "Highlights from GP Refresh in Brisbane, Melbourne, Sydney and the Gold Coast. Delegates rate GP Refresh 9.7 out of 10.",
          [], [pill(REGISTER, "Join us in 2027", "gold", True), pill("https://www.youtube.com/@GPRefreshConference", "YouTube channel", "", True)])
     + f'<section class="gpr-section" style="padding-top:0"><div class="gpr-wrap">{"".join(blocks)}</div></section>'
     + register_band("2027 · Melbourne · Sydney · Brisbane", "Be part of the next one.", "Group discounts of up to 65% end 30 December."))

# ============================ About Us ============================
RRR = [("Refresh the basics.", [("Innovative clinical approaches", "New methods and technologies in patient care."),
                                 ("Continuing medical education", "The latest guidelines and best practice."),
                                 ("Stronger patient relationships", "Communication that builds trust."),
                                 ("Work-life balance", "Self-care and preventing burnout.")]),
       ("Reframe the evidence.", [("Patient-centred care", "New perspectives on consults and treatment plans."),
                                  ("Cultural competence", "Understanding diverse patient backgrounds."),
                                  ("Latest research in primary care", "Studies that change general practice."),
                                  ("Collaborative care", "Working with other health professionals.")]),
       ("Reignite your passion for patient care.", [("Stories from the field", "Reminders of why we chose medicine."),
                                                    ("Mentorship and leadership", "A culture of guidance among GPs."),
                                                    ("Advocacy for change", "GPs in health policy discussions."),
                                                    ("Mental health in primary care", "Resources GPs and patients need.")])]
rrr = [f'<li><article class="gpr-card{" gpr-card--dark" if i == 1 else ""}"><p class="gpr-eyebrow" style="font-size:11px{";color:var(--gpr-gold)" if i == 1 else ""}">{["Refresh", "Reframe", "Reignite"][i]}</p>'
       f'<h3 style="margin-top:10px">{e(t)}</h3><ul>{"".join(f"<li><b>{e(a)}</b>{e(b)}</li>" for a, b in pts)}</ul></article></li>' for i, (t, pts) in enumerate(RRR)]
TEAM = [("Dr Kish Nallapu", "Founder & Convenor", ""), ("Anis Nicolas Haddad", "Director, Strategy & Partnerships", "directorpartnerships@gprefresh.com"),
        ("Kasey Joines", "Events Manager", "eventsmanager@gprefresh.com"), ("Amal Bose", "CPD, Delegate & Speaker Manager", "cpd@gprefresh.com")]
team = "".join(f'<li><b>{e(n)}</b><span>{e(r)}</span>{f"<em>{m}</em>" if m else ""}</li>' for n, r, m in TEAM)
page("about.html", "About GP Refresh", "GP Refresh, The Global Family Doctors Congress: practical, independent CPD for GPs, guided by a Scientific Committee and Advisory Committee of leading clinicians.",
     hero("About Us", "GP Refresh · The Global Family Doctors Congress", "Practical education that fits the realities of practice.",
          "GP Refresh brings the best minds in primary care together to share practical insights, emerging treatments and current guidelines, in 6-minute talks GPs can apply the next day.") + f"""
<section class="gpr-section">
  <div class="gpr-wrap gpr-program__grid">
    <div class="gpr-prose">
      <p class="gpr-eyebrow">Who we are</p>
      <h2 class="gpr-title">Built by clinicians, for clinicians.</h2>
      <p style="margin-top:22px">GP Refresh is run by healthcare professionals with decades of combined experience in clinical practice, medical education and professional development. We understand the pressures of modern general practice, so we keep learning concise, relevant and directly applicable.</p>
      <p>Our program is guided by a Scientific Committee and an Advisory Committee of experienced clinicians, specialists and educators. Their oversight keeps every session evidence-based, clinically rigorous and independent.</p>
      <p>We welcome everyone working in primary care, including GPs, GP registrars, non-GP specialists, hospital doctors, nurses and allied health professionals with an AHPRA number.</p>
    </div>
    <div class="gpr-days">
      <a class="gpr-card gpr-card--dark" href="advisory-committee.html" style="text-decoration:none"><p class="gpr-eyebrow" style="font-size:11px;color:var(--gpr-gold)">Governance</p><h3 style="margin-top:8px">Advisory Committee →</h3></a>
      <a class="gpr-card" href="melbourne.html#committee" style="text-decoration:none;color:inherit"><p class="gpr-eyebrow" style="font-size:11px">Program</p><h3 style="margin-top:8px">Scientific Committee →</h3></a>
      <a class="gpr-card" href="past-congresses.html" style="text-decoration:none;color:inherit"><p class="gpr-eyebrow" style="font-size:11px">Since 2025</p><h3 style="margin-top:8px">Past Congresses →</h3></a>
    </div>
  </div>
</section>

<section class="gpr-section gpr-committee" aria-labelledby="rrr-title">
  <div class="gpr-wrap gpr-head"><div><p class="gpr-eyebrow">Refresh · Reframe · Reignite</p><h2 class="gpr-title" id="rrr-title">What GP Refresh is for.</h2></div>{rail_nav('rrr')}</div>
  {rail('rrr', rrr)}
</section>

<section class="gpr-section" aria-labelledby="team-title">
  <div class="gpr-wrap">
    <p class="gpr-eyebrow">The team</p>
    <h2 class="gpr-title" id="team-title">The people behind every Congress.</h2>
    <ul class="gpr-grid gpr-grid--4 gpr-team" style="margin-top:28px">{team}</ul>
  </div>
</section>
""" + register_band("GP Refresh Congress 2027", "Join the 6-Minute GP Refresh CPD Revolution.", "Melbourne, Sydney and Brisbane. Up to 53 CPD hours."))

# ============================ Advisory Committee ============================
ADV = [("dr-justin", "Dr Justin Coleman", "Editor, Murtagh's General Practice 9th Ed."), ("dr-nicole", "Dr Nicole Higgins", "Past RACGP President"),
       ("dr-bruce", "Dr Bruce Willett", "Past RACGP Vice-President"), ("dr-ian", "Dr Ian Kamerman", "Specialist GP"),
       ("dr-naveen", "Dr Naveen Somia", "Specialist Plastic Surgeon"), ("dr-prakash", "Dr Prakash Appanna", "Experienced GP")]
page("advisory-committee.html", "GP Refresh Advisory Committee", "Meet the GP Refresh Advisory Committee: leading clinicians who guide the direction of GP Refresh Congress.",
     hero("Advisory Committee", "Governance", "Meet the GP Refresh Advisory Committee.",
          "Experienced clinicians and educators who guide the direction of GP Refresh and keep it focused on what matters in everyday practice.") + f"""
<section class="gpr-section gpr-committee" aria-labelledby="adv-title">
  <div class="gpr-wrap gpr-head"><div><p class="gpr-eyebrow">Advisory Committee</p><h2 class="gpr-title" id="adv-title">Six clinicians. One purpose.</h2></div>{rail_nav('adv')}</div>
  {rail('adv', [person(*a) for a in ADV])}
</section>
<section class="gpr-section">
  <div class="gpr-wrap gpr-prose">
    <p class="gpr-eyebrow">Scientific Committee</p>
    <h2 class="gpr-title">The program is set by our Scientific Committee.</h2>
    <p class="gpr-lede">Chaired by Dr Justin Coleman, the Scientific Committee selects every clinical topic and reviews every talk.</p>
    <div class="gpr-price__ctas">{pill("melbourne.html#committee", "Meet the Scientific Committee")}</div>
  </div>
</section>
""")

# ============================ FAQs ============================
FAQ = [("For delegates", [
    ("I'm not a GP. Can I still attend and claim CPD hours?", "Yes. GP Refresh welcomes any medical practitioner, including non-GP specialists and hospital doctors, as well as registered nurses and allied health professionals with an AHPRA number."),
    ("How many CPD hours can I earn?", "Up to 53 CPD hours, by attending the full Congress and completing the pre- and post-Congress activities. RACGP CPD Home hours are allocated directly by GP Refresh. For other CPD homes, we provide confirmation for you to upload."),
    ("Is GP Refresh accredited?", "Yes. GP Refresh is an accredited CPD provider with RACGP and ACRRM, and RNZCGP members can claim up to 80 CME credits. Certificates are provided."),
    ("What is a 6-minute talk?", "Leading clinicians distil a 1-hour lecture into a 6-minute TED-style talk with one clear learning outcome. There are 70+ clinical topics across two days."),
    ("Are sessions interactive?", "Yes. During each block of talks, delegates send questions through the GP Refresh app. The questions are answered in the 30-minute panel discussion that follows."),
    ("Are there sponsored talks?", "No. Every talk is independent and evidence-based, with no commercial influence over what you learn."),
    ("Will session recordings be available?", "Yes. Recordings are available to registered delegates for 4 weeks after the Congress."),
    ("Can I attend online?", "Yes. GP Refresh offers online attendance options."),
    ("Is the Gala Dinner included?", "Yes. The Grand Gala Dinner & Show on Saturday night (valued at $329) is included with every Congress Pass. Additional guest tickets can be added during registration."),
    ("Is there a CPR session?", "Yes. The CPR Workshop on Saturday afternoon is included for every delegate."),
    ("Are group discounts available?", "Yes. Book 2 or more GPs together and save 52%, rising to 55% for 5+, 60% for 10+ and 65% for 15+ GPs. Group discounts end 30 December."),
    ("Are accommodation discounts available?", "Yes. Discounted accommodation packages will be announced for each city."),
    ("When and where are future Congresses held?", "In 2027: Melbourne (15–16 May), Sydney (26–27 June) and Brisbane (18–19 Sept). International Cruises and Dubai dates are to be confirmed."),
]), ("For industry partners", [
    ("What partnership packages are available?", "Diamond, Platinum and Gold partnership packages, plus standard and non-profit exhibition booths. Pricing and inclusions are in the 2027 Partnership Prospectus, available on request."),
    ("How do partners meet delegates?", "Every catering break is held in the Exhibition Hall: 7 breaks and about 6 hours of face-to-face time at each Congress."),
    ("Can we exhibit in more than one city?", "Yes. Book two Congresses and save 8%, or all three and save 16% with Official National Partner status."),
    ("When will logistical details be provided?", "An Exhibitor Manual is sent before each Congress, covering bump-in and bump-out times, venue access, freight and on-site requirements."),
    ("Are there compliance requirements?", "Yes. All partner activity must comply with relevant industry regulations. Partners are responsible for making sure their materials meet applicable standards."),
    ("How do we secure a partnership?", "A partnership is confirmed when we receive a signed agreement and payment. Space is limited and allocated first come, first served."),
])]
groups = "".join(f'<div class="gpr-faq-group"><h2>{g}</h2>' + "".join(f'<details class="gpr-faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in qs) + "</div>" for g, qs in FAQ)
ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for _, qs in FAQ for q, a in qs]}, ensure_ascii=False)
page("faqs.html", "GP Refresh FAQs", "Answers to common questions about GP Refresh Congress 2027: CPD hours, accreditation, the 6-minute format, Gala Dinner, group discounts and partnerships.",
     hero("FAQs", "Frequently asked questions", "Everything you need to know.",
          "Can't find your answer? Call 1300 GP REFRESH (1300 477 337) or email connect@gprefresh.com.") +
     f'<section class="gpr-section" style="padding-top:0"><div class="gpr-wrap" style="max-width:900px">{groups}</div></section>',
     extra_head=f'<script type="application/ld+json">{ld}</script>\n')

# ============================ Contact ============================
page("contact.html", "Contact GP Refresh", "Contact GP Refresh: phone 1300 GP REFRESH (1300 477 337), email connect@gprefresh.com, or reach the events, CPD and partnerships teams directly.",
     hero("Contact Us", "Get in touch", "We're here to help.",
          "Questions about registration, CPD, speaking or partnering? Contact the right team below.") + """
<section class="gpr-section" style="padding-top:0">
  <div class="gpr-wrap">
    <ul class="gpr-grid">
      <li class="gpr-card"><p class="gpr-eyebrow" style="font-size:11px">General enquiries</p><h3 style="margin-top:8px">1300 GP REFRESH</h3>
        <ul><li><b>Phone</b><span style="user-select:all">1300 477 337</span></li><li><b>Email</b><span style="user-select:all">connect@gprefresh.com</span></li></ul></li>
      <li class="gpr-card"><p class="gpr-eyebrow" style="font-size:11px">Delegates &amp; speakers</p><h3 style="margin-top:8px">CPD team</h3>
        <ul><li><b>CPD, delegates &amp; speakers</b><span style="user-select:all">cpd@gprefresh.com</span></li><li><b>Events</b><span style="user-select:all">eventsmanager@gprefresh.com</span></li></ul></li>
      <li class="gpr-card gpr-card--dark"><p class="gpr-eyebrow" style="font-size:11px;color:var(--gpr-gold)">Industry partners</p><h3 style="margin-top:8px">Partnerships</h3>
        <ul><li><b>Strategy &amp; partnerships</b><span style="user-select:all">directorpartnerships@gprefresh.com</span></li><li><b>Prospectus</b>Ask for the 2027 Partnership Prospectus</li></ul></li>
    </ul>
  </div>
</section>
<section class="gpr-section gpr-committee">
  <div class="gpr-wrap gpr-prose">
    <p class="gpr-eyebrow">Congress organiser</p>
    <h2 class="gpr-title">The Production House Events</h2>
    <p class="gpr-lede">03 9020 7055 · info@tphe.com.au<br>38 Old Burleigh Rd, Surfers Paradise QLD 4217</p>
  </div>
</section>
""")
