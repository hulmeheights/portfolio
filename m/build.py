"""Build premium homepage mockups for leads.
python m/build.py leads.json OUT_DIR HERO_BASE_URL   ->  OUT_DIR/<slug>/index.html, prints [{id, slug}]
leads.json: [{id,name,trade,area,phone,rating,reviews,address}]

Five art directions, picked by trade family (see trades.py):
  dark  - "after hours": espresso black, brass, tall condensed display (barbers, tattoo, valeting, PT, mechanics)
  blush - "atelier": rose paper, oxblood ink, light high-contrast serif (nails, beauty, hair, florists, aesthetics)
  fresh - "out the door": sage, forest ink, soft rounded serif (dog groomers, walkers, gardens, windows)
  navy  - "site ready": concrete, navy, hi-vis orange, wide grotesk (trades and builders)
  warm  - "counter": flour cream, walnut ink, olive, friendly serif (cafes, bakeries, massage, joinery, decorating)
The memorable thing on every page is the business's own name, set huge over their trade's photo.
"""
import html, json, os, re, sys
import trades
IMGDIR = "m/_img"

STYLES = {
 "dark": dict(bg="#17130f", ink="#efe6d6", mute="#a89c8a", acc="#b8935a", panel="#211b15", line="#3a3128",
   fonts="Big+Shoulders+Display:wght@700;900&family=Manrope:wght@400;500;700",
   disp="'Big Shoulders Display',Impact,sans-serif", body="Manrope,system-ui,sans-serif",
   dw="900", dsize="clamp(64px,17vw,188px)", dlh=".86", dtrack="-.005em", dcase="uppercase", heroshade="rgba(23,19,15,.92)"),
 "blush": dict(bg="#f6eee8", ink="#3b2328", mute="#8a6f70", acc="#8f3f4c", panel="#efe2da", line="#dcc9c0",
   fonts="Cormorant:ital,wght@0,400;0,500;1,400&family=Jost:wght@400;500",
   disp="Cormorant,Georgia,serif", body="Jost,system-ui,sans-serif",
   dw="400", dsize="clamp(58px,14vw,168px)", dlh=".9", dtrack="-.02em", dcase="none", heroshade="rgba(59,35,40,.78)"),
 "fresh": dict(bg="#edf0e4", ink="#1d2b21", mute="#5d6b5f", acc="#c98f1e", panel="#e1e7d4", line="#c9d1b9",
   fonts="Fraunces:opsz,wght,SOFT@9..144,600,100&family=DM+Sans:wght@400;500;700",
   disp="Fraunces,Georgia,serif", body="'DM Sans',system-ui,sans-serif",
   dw="600", dsize="clamp(54px,13vw,150px)", dlh=".92", dtrack="-.03em", dcase="none", heroshade="rgba(29,43,33,.82)",
   dextra="font-variation-settings:'SOFT' 100;"),
 "navy": dict(bg="#eeece6", ink="#13203a", mute="#5b6475", acc="#ff6b1a", panel="#e2dfd6", line="#cfcbc0",
   fonts="Archivo:wdth,wght@62..125,400;62..125,600;62..125,800",
   disp="Archivo,system-ui,sans-serif", body="Archivo,system-ui,sans-serif",
   dw="800", dsize="clamp(48px,11vw,132px)", dlh=".9", dtrack="-.02em", dcase="none", heroshade="rgba(19,32,58,.86)",
   dextra="font-stretch:125%;"),
 "warm": dict(bg="#f4ecdf", ink="#2e2117", mute="#7b6857", acc="#6f7d3c", panel="#ebe0cf", line="#d8c9b2",
   fonts="Young+Serif&family=Figtree:wght@400;500;700",
   disp="'Young Serif',Georgia,serif", body="Figtree,system-ui,sans-serif",
   dw="400", dsize="clamp(52px,12.5vw,146px)", dlh=".94", dtrack="-.02em", dcase="none", heroshade="rgba(46,33,23,.82)"),
}

def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:48]
def nice_phone(p):
    d = re.sub(r"\D", "", p or "")
    if d.startswith("44"): d = "0" + d[2:]
    return (d[:5] + " " + d[5:]) if len(d) == 11 else (p or "")

PAGE = """<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>{name}, {area}</title>
<link rel="stylesheet" href="/m/_fonts/fonts.css">
<style>
:root{{--bg:{bg};--ink:{ink};--mute:{mute};--acc:{acc};--panel:{panel};--line:{line};--disp:{disp};--body:{body}}}
*{{box-sizing:border-box;margin:0;padding:0}}html{{scroll-behavior:smooth}}
body{{background:var(--bg);color:var(--ink);font:400 17px/1.6 var(--body);-webkit-font-smoothing:antialiased}}
a{{color:inherit;text-decoration:none}}img{{display:block;max-width:100%}}
:focus-visible{{outline:2px solid var(--acc);outline-offset:3px}}
.w{{width:min(1180px,100% - 40px);margin-inline:auto}}
.disp{{font-family:var(--disp);font-weight:{dw};letter-spacing:{dtrack};text-transform:{dcase};{dextra}}}
.concept{{font-size:12px;color:var(--mute);text-align:center;padding:8px 16px;border-bottom:1px solid var(--line)}}
.nav{{display:flex;justify-content:space-between;align-items:center;padding:18px 0}}
.nav .mark{{font-size:22px;line-height:1}}
.pill{{display:inline-flex;align-items:center;justify-content:center;gap:10px;border-radius:999px;padding:14px 22px;font-weight:600;font-size:15px;background:var(--acc);color:#fff;transition:transform .15s}}
.pill:active{{transform:scale(.97)}}.pill.line{{background:transparent;color:inherit;border:1px solid currentColor}}
.hero{{position:relative;min-height:min(84svh,860px);display:grid;align-items:end;overflow:hidden;color:#fff;isolation:isolate}}
.hero img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2;transform:scale(1.06);animation:settle 1.6s cubic-bezier(.2,.7,.2,1) forwards}}
.hero:after{{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(0,0,0,0) 25%,{heroshade} 88%)}}
@keyframes settle{{to{{transform:scale(1)}}}}
.hero .w{{padding:0 0 clamp(28px,6vw,64px)}}
.name{{font-size:{dsize};line-height:{dlh};max-width:11ch;overflow-wrap:anywhere}}
.sub{{display:flex;flex-wrap:wrap;gap:14px 28px;align-items:end;justify-content:space-between;margin-top:clamp(18px,3vw,30px)}}
.sub p{{font-size:clamp(18px,2.2vw,22px);max-width:30ch;line-height:1.4}}
.stars{{font-size:15px;opacity:.9;margin-top:10px}}.stars b{{color:#f2c46d;letter-spacing:3px;font-weight:400}}
.ctas{{display:flex;gap:10px;flex-wrap:wrap}}.hero .pill.line{{border-color:rgba(255,255,255,.6)}}
.sec{{padding:clamp(64px,10vw,120px) 0}}
.h2{{font-size:clamp(40px,7vw,84px);line-height:.95;margin-bottom:clamp(28px,4vw,48px);max-width:14ch}}
.list{{border-top:1px solid var(--line)}}
.list a{{display:grid;grid-template-columns:1fr auto;gap:16px;align-items:baseline;padding:22px 2px;border-bottom:1px solid var(--line)}}
.list .s{{font-size:clamp(26px,4.4vw,46px);line-height:1.05}}.list .q{{font-size:14px;color:var(--mute);white-space:nowrap}}
.list a:hover .s{{color:var(--acc)}}
.split{{display:grid;gap:clamp(32px,5vw,72px);grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));align-items:center}}
.split .copy p{{color:var(--mute);max-width:42ch;margin-top:16px}}
.phone{{background:var(--panel);border:1px solid var(--line);border-radius:36px;padding:26px 20px 30px;max-width:380px;justify-self:center;width:100%}}
.phone .top{{display:flex;justify-content:space-between;font-size:13px;color:var(--mute);margin-bottom:22px}}
.msg{{background:#fff;color:#1b1b1b;border-radius:20px 20px 20px 6px;padding:14px 16px;font-size:15px;line-height:1.45;box-shadow:0 10px 30px -18px rgba(0,0,0,.35)}}
.msg small{{display:block;color:#8a8a8a;font-size:12px;margin-top:6px}}
.missed{{display:flex;align-items:center;gap:10px;font-size:13px;color:var(--mute);margin:0 0 12px 4px}}
.missed:before{{content:"";width:8px;height:8px;border-radius:50%;background:#d64545}}
.form{{display:flex;gap:8px;margin-top:22px;flex-wrap:wrap}}
.form input{{flex:1 1 180px;min-width:0;border:1px solid var(--line);background:var(--bg);color:var(--ink);border-radius:999px;padding:14px 18px;font:inherit}}
.proof{{background:var(--ink);color:var(--bg)}}
.big{{font-size:clamp(120px,30vw,320px);line-height:.8}}
.proof .split p{{color:color-mix(in srgb,var(--bg) 70%,transparent);font-size:clamp(20px,2.6vw,28px);line-height:1.35;max-width:24ch}}
.local{{display:grid;gap:28px;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr))}}
.local h3{{font-size:clamp(26px,3vw,34px);line-height:1.05;margin-bottom:10px}}.local p{{color:var(--mute)}}
footer{{border-top:1px solid var(--line);padding:clamp(56px,8vw,96px) 0 120px}}
footer .tel{{font-size:clamp(44px,9vw,112px);line-height:.95;display:block;margin:10px 0 26px}}
footer .meta{{display:flex;flex-wrap:wrap;gap:10px 32px;color:var(--mute);font-size:15px}}
.dock{{transform:translateY(140%);transition:transform .35s cubic-bezier(.2,.7,.2,1)}}.dock.on{{transform:none}}.dock{{position:fixed;inset:auto 12px 12px;display:flex;gap:8px;padding:8px;border-radius:999px;background:color-mix(in srgb,var(--ink) 92%,transparent);backdrop-filter:blur(10px);z-index:9}}
.dock .pill{{flex:1;padding:13px 10px}}.dock .pill.line{{color:var(--bg)}}
@media(min-width:860px){{.dock{{display:none}}footer{{padding-bottom:72px}}}}
@media(prefers-reduced-motion:reduce){{.hero img{{animation:none;transform:none}}html{{scroll-behavior:auto}}}}
</style></head><body>
<div class="concept">A homepage idea for {name}, made by HulmeHeights</div>
<header class="w nav"><a class="mark disp" href="#">{short}</a><a class="pill" href="tel:{tel}">Call</a></header>
<section class="hero"><img src="{hero}" alt="" fetchpriority="high"><div class="w">
<h1 class="name disp">{name}</h1>
<div class="sub"><div><p>{tagline} {trade_line}</p>{stars}</div>
<div class="ctas"><a class="pill" href="tel:{tel}">Call {phone}</a><a class="pill line" href="#text">Text me back</a></div></div></div></section>
<section class="sec"><div class="w"><h2 class="h2 disp">{services_title}</h2><nav class="list">{services}</nav></div></section>
<section class="sec" id="text" style="padding-top:0"><div class="w split">
<div class="copy"><h2 class="h2 disp" style="margin-bottom:0">Missed us? We'll text you back.</h2>
<p>When we're with a customer and can't get to the phone, you get a text within a minute, so you're never left wondering if anyone got your call.</p>
<form class="form" onsubmit="this.innerHTML='<p style=&quot;color:var(--ink)&quot;>Got it. You\\u2019ll get a text from {short_js} in a minute.</p>';return false">
<label for="n" style="position:absolute;left:-9999px">Your mobile number</label><input id="n" type="tel" inputmode="tel" placeholder="Your mobile number" required><button class="pill" type="submit">Text me back</button></form></div>
<div class="phone" aria-hidden="true"><div class="top"><span>Messages</span><span>now</span></div>
<div class="missed">Missed call from you</div>
<div class="msg">Hi, it's {short} here. Sorry we missed you, we're with a customer. What can we help with? We'll ring you back shortly.<small>Delivered</small></div></div>
</div></section>
{proof}
<section class="sec"><div class="w"><h2 class="h2 disp">Here for {area}.</h2><div class="local">
<div><h3 class="disp">Close by</h3><p>Based locally, so we can get to you quickly and we know the area well.</p></div>
<div><h3 class="disp">Straight answers</h3><p>Clear prices before we start. No surprises at the end.</p></div>
<div><h3 class="disp">Easy to reach</h3><p>Call, text, or leave your number and we'll come back to you the same day.</p></div></div></div></section>
<footer><div class="w"><span class="disp" style="font-size:22px">{name}</span><a class="tel disp" href="tel:{tel}">{phone}</a>
<div class="meta"><span>{address}</span><span>{area}</span></div></div></footer>
<div class="dock" id="dock"><a class="pill" href="tel:{tel}">Call</a><a class="pill line" href="#text">Text me back</a></div>
<script>new IntersectionObserver(([e])=>document.getElementById('dock').classList.toggle('on',!e.isIntersecting)).observe(document.querySelector('.hero'))</script>
</body></html>"""

PROOF = """<section class="sec proof"><div class="w split"><div class="big disp">{rt}</div>
<p>Rated {rt} out of 5 by {rv} customers on Google. Read them before you book. We think you'll like what you see.</p></div></section>"""

SERVICES_TITLE = {"dark": "What we do", "blush": "Treatments", "fresh": "How we help", "navy": "The work", "warm": "What we do"}

def short_name(n):
    n = re.sub(r"\b(ltd|limited|llp)\b\.?", "", n, flags=re.I).strip(" ,-")
    return n if len(n) <= 24 else " ".join(n.split()[:3])

def page(l, hero_base):
    c = trades.get(l.get("trade")); fam = c["family"]; S = STYLES[fam]; e = lambda s: html.escape(str(s or ""), quote=True)
    area = l.get("area") or "the area"; tr = (l.get("trade") or "").strip().lower()
    base = (tr if tr in trades.T else 'default').replace(' ', '-')
    opts = [f"hero-{base}.jpg"] + [f"hero-{base}-{k}.jpg" for k in (2, 3) if os.path.exists(os.path.join(IMGDIR, f"hero-{base}-{k}.jpg"))]
    hero = f"{hero_base}/{opts[int(l.get('id') or 0) % len(opts)]}"
    rv = int(l.get("reviews") or 0); rt = float(l.get("rating") or 0); good = rv >= 8 and rt >= 4.3
    stars = f'<div class="stars"><b>★★★★★</b> {rt:.1f} on Google, {rv} reviews</div>' if good else ""
    proof = PROOF.format(rt=f"{rt:.1f}", rv=rv) if good else ""
    svc = "".join(f'<a href="#text"><span class="s disp">{e(s)}</span><span class="q">Ask for a price</span></a>' for s in c["services"])
    tel = re.sub(r"[^\d+]", "", l.get("phone") or "")
    nm = l["name"]; sh = short_name(nm)
    return PAGE.format(fonts=S["fonts"], bg=S["bg"], ink=S["ink"], mute=S["mute"], acc=S["acc"], panel=S["panel"], line=S["line"],
        disp=S["disp"], body=S["body"], dw=S["dw"], dsize=S["dsize"], dlh=S["dlh"], dtrack=S["dtrack"], dcase=S["dcase"],
        dextra=S.get("dextra", ""), heroshade=S["heroshade"], name=e(nm), short=e(sh), short_js=e(sh).replace("'", "\\'"),
        area=e(area), hero=hero, tel=tel, phone=e(nice_phone(l.get("phone"))), tagline=e(c["tagline"]),
        trade_line=e(f"{(l.get('trade') or 'Local business').capitalize()} in {area}."), stars=stars, proof=proof,
        services_title=SERVICES_TITLE[fam], services=svc, address=e(l.get("address")))

if __name__ == "__main__":
    leads = json.load(open(sys.argv[1])); out = sys.argv[2]; base = sys.argv[3]; done = []
    IMGDIR = os.path.join(out, "_img")
    for l in leads:
        if l["name"] == l["name"].lower() or (l["name"] == l["name"].upper() and len(l["name"]) > 5): l["name"] = l["name"].title()
        s = l.get("slug") or slug(f"{l['name']}-{l.get('area') or ''}") or str(l["id"])
        os.makedirs(os.path.join(out, s), exist_ok=True)
        open(os.path.join(out, s, "index.html"), "w").write(page(l, base)); done.append({"id": l["id"], "slug": s})
    print(json.dumps(done))
