"""Congress + Exhibition pages for locations still to be confirmed (Int'l Cruises, Dubai).
They hold the place in the menu, show what is known and collect interest.
Run: python3 -I _build/make_tbc.py"""
import html, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location("pages", os.path.join(os.path.dirname(os.path.abspath(__file__)), "make_pages_lib.py"))
lib = importlib.util.module_from_spec(spec); spec.loader.exec_module(lib)
e = html.escape

LOC = {
    "cruises": dict(name="Int'l Cruises", full="GP Refresh International Cruises", when="December 2027", whenshort="Dec 2027",
                    where="Itinerary to be confirmed", lead="Learn at sea. The 6-minute CPD Revolution goes international.",
                    note="Dates, ship and itinerary are being finalised."),
    "dubai": dict(name="Dubai", full="GP Refresh Dubai", when="8–9 January 2028", whenshort="8–9 Jan 2028",
                  where="Venue to be confirmed", lead="The Global Family Doctors Congress comes to Dubai.",
                  note="Dates are provisional and the venue is being finalised."),
}

def tbc_hero(crumb, eyebrow, h1, lede, metas, ctas):
    m = "".join(f"<li>{x}</li>" for x in metas)
    return f"""
<section class="gpr-section gpr-cpd gpr-on-dark gpr-wave gpr-wave--tr" style="padding-block:clamp(48px,8vw,96px)">
  <div class="gpr-wrap">
    <p class="gpr-crumb" style="color:rgba(255,255,255,.7)"><a href="index.html" style="color:var(--gpr-gold)">Home</a> · {e(crumb)}</p>
    <p class="gpr-eyebrow">{eyebrow}</p>
    <h1 class="gpr-title" style="font-size:clamp(34px,5.4vw,60px);line-height:1.1;color:#fff;max-width:18ch">{h1}</h1>
    <p class="gpr-lede">{lede}</p>
    <ul class="gpr-loc-meta">{m}</ul>
    <div class="gpr-loc-hero__ctas">{''.join(ctas)}</div>
  </div>
</section>"""

def interest(title, lede, ask):
    return f"""
<section class="gpr-section" id="interest">
  <div class="gpr-wrap">
    <p class="gpr-eyebrow">Register your interest</p>
    <h2 class="gpr-title">{title}</h2>
    <p class="gpr-lede">{lede}</p>
    <ul class="gpr-enquire">
      <li><small>Email</small><b>connect@gprefresh.com</b></li>
      <li><small>Phone</small><b>1300 477 337</b></li>
      <li><small>Ask for</small><b>{ask}</b></li>
    </ul>
  </div>
</section>"""

for key, L in LOC.items():
    meta = [f"<b>{e(L['whenshort'])}</b> <span class=\"gpr-tbc\">TBC</span>", e(L["where"])]
    # ---------- Congress page ----------
    body = tbc_hero(f"Congress · {L['name']}", f"{e(L['full'])} · to be confirmed", e(L["lead"]),
                    f"{e(L['note'])} Register your interest and we'll tell you first when registrations open.", meta,
                    [lib.pill("#interest", "Register interest", "gold"), lib.pill("index.html#congresses", "2027 Australian Congresses")])
    body += f"""
<section class="gpr-section">
  <div class="gpr-wrap">
    <p class="gpr-eyebrow">What to expect</p>
    <h2 class="gpr-title">The same 6-minute format GPs rate 9.7 out of 10.</h2>
    <ul class="gpr-grid" style="margin-top:28px">
      <li class="gpr-card"><h3>6-minute talks</h3><ul><li>Leading clinicians distil a 1-hour lecture into a 6-minute TED-style talk, each with a clear learning outcome.</li></ul></li>
      <li class="gpr-card"><h3>Panel discussions</h3><ul><li>Delegate questions answered by the experts after every block of talks.</li></ul></li>
      <li class="gpr-card gpr-card--dark"><h3>CPD details</h3><ul><li>CPD hours and accreditation for {e(L['name'])} will be confirmed with the program.</li></ul></li>
    </ul>
  </div>
</section>""" + interest(f"Be first to hear about {e(L['name'])}.",
                         "Contact the GP Refresh team and we'll add you to the list for dates, program and pricing.",
                         f"{e(L['name'])} delegate updates")
    lib.page(f"{key}.html", f"{L['full']}", f"{L['full']}: {L['when']} (to be confirmed). Register your interest for the 6-minute GP Refresh CPD format.", body)

    # ---------- Exhibition page ----------
    body = tbc_hero(f"Exhibition · {L['name']}", f"{e(L['full'])} · exhibition · to be confirmed", f"Partner with GP Refresh in {e(L['name'])}.",
                    f"{e(L['note'])} Partnership details will follow once the program is confirmed.", meta,
                    [lib.pill("#interest", "Register partner interest", "gold"), lib.pill("exhibition-melbourne.html", "2027 Australian exhibitions")])
    body += f"""
<section class="gpr-section">
  <div class="gpr-wrap gpr-program__grid">
    <div>
      <p class="gpr-eyebrow">How GP Refresh works for partners</p>
      <h2 class="gpr-title">Every break is spent in the Exhibition Hall.</h2>
      <p class="gpr-lede">In Australia, every catering break is served among the booths: 7 breaks and about 6 hours face to face with GPs at each Congress. The {e(L['name'])} format will be confirmed with the program.</p>
    </div>
    <div class="gpr-photo"><img src="assets/img/hall-02.jpg" alt="Delegates talking over coffee in the GP Refresh Exhibition Hall" loading="lazy"></div>
  </div>
</section>""" + interest(f"Register partner interest for {e(L['name'])}.",
                         "Contact the partnerships team and we'll send details as soon as they're confirmed.",
                         f"{e(L['name'])} partnership details")
    lib.page(f"exhibition-{key}.html", f"GP Refresh Exhibition {L['name']}", f"Exhibit at {L['full']}, {L['when']} (to be confirmed). Register partner interest.", body)
