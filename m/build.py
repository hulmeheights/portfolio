"""Build homepage mockups for leads.  python build.py leads.json OUT_DIR HERO_BASE_URL
leads.json: [{id,name,trade,area,phone,rating,reviews,address,maps_url}]  -> OUT_DIR/<slug>/index.html, returns slugs."""
import html, json, os, re, sys
import trades
def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:48]
def nice_phone(p):
    d = re.sub(r"\D", "", p or "")
    if d.startswith("44"): d = "0" + d[2:]
    return (d[:5] + " " + d[5:]) if len(d) == 11 else (p or "")
def stars(r):
    r = float(r or 0); full = int(round(r)); return "★" * full + "☆" * (5 - full)

PAGE = """<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>{name} | {area}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--bg:{bg};--ink:{ink};--acc:{acc};--soft:{soft}}}
*{{box-sizing:border-box;margin:0}}body{{background:var(--bg);color:var(--ink);font:16px/1.55 Inter,system-ui,sans-serif}}
a{{color:inherit;text-decoration:none}}.wrap{{max-width:1080px;margin:0 auto;padding:0 20px}}
.concept{{background:var(--acc);color:#fff;font-size:12px;text-align:center;padding:6px 10px;letter-spacing:.02em}}
header{{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid color-mix(in srgb,var(--ink) 10%,transparent)}}
header .wrap{{display:flex;align-items:center;justify-content:space-between;height:62px}}
.logo{{font:600 20px/1 Fraunces,serif;letter-spacing:-.01em}}
.btn{{display:inline-flex;align-items:center;gap:8px;background:var(--acc);color:#fff;font-weight:600;padding:12px 18px;border-radius:999px;font-size:15px}}
.btn.ghost{{background:transparent;color:var(--ink);border:1.5px solid color-mix(in srgb,var(--ink) 25%,transparent)}}
.hero{{position:relative;min-height:78vh;display:flex;align-items:flex-end;color:#fff;background:#111 url({hero}) center/cover}}
.hero:before{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.15),rgba(0,0,0,.72))}}
.hero .wrap{{position:relative;padding-bottom:56px;padding-top:120px}}
.kick{{font-size:13px;text-transform:uppercase;letter-spacing:.14em;opacity:.85}}
h1{{font:600 clamp(38px,8vw,72px)/1.02 Fraunces,serif;letter-spacing:-.02em;margin:12px 0 14px;max-width:14ch}}
.lede{{font-size:18px;max-width:34ch;opacity:.92}}
.rate{{margin-top:16px;font-size:15px}}.rate b{{color:#ffd36b;letter-spacing:2px}}
.ctas{{display:flex;gap:10px;flex-wrap:wrap;margin-top:24px}}.hero .btn.ghost{{color:#fff;border-color:rgba(255,255,255,.5)}}
section{{padding:64px 0}}h2{{font:600 clamp(28px,5vw,40px)/1.1 Fraunces,serif;letter-spacing:-.01em;margin-bottom:22px}}
.svc{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}}
.svc div{{background:var(--soft);border-radius:16px;padding:22px 20px;font-weight:600}}.svc small{{display:block;font-weight:400;opacity:.7;margin-top:4px}}
.missed{{background:var(--ink);color:var(--bg);border-radius:24px;padding:28px;display:grid;gap:14px}}
.missed h3{{font:600 26px/1.15 Fraunces,serif}}.missed p{{opacity:.8}}
.missed form{{display:flex;gap:8px;flex-wrap:wrap}}.missed input{{flex:1 1 200px;padding:14px 16px;border-radius:999px;border:0;font:inherit}}
.why{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:22px}}.why b{{display:block;font:600 20px Fraunces,serif;margin-bottom:6px}}
footer{{background:var(--soft);padding:40px 0 90px;font-size:15px}}footer .wrap{{display:grid;gap:8px}}
.bar{{position:fixed;left:0;right:0;bottom:0;display:flex;gap:8px;padding:10px 12px;background:var(--bg);border-top:1px solid color-mix(in srgb,var(--ink) 12%,transparent);z-index:9}}
.bar a{{flex:1;justify-content:center}}@media(max-width:480px){{.hp{{display:none}}}}@media(min-width:800px){{.bar{{display:none}}footer{{padding-bottom:40px}}}}
</style></head><body>
<div class="concept">Homepage concept made for {name} by HulmeHeights</div>
<header><div class="wrap"><a class="logo" href="#">{name}</a><a class="btn" href="tel:{tel}">Call<span class="hp"> {phone_short}</span></a></div></header>
<div class="hero"><div class="wrap"><div class="kick">{trade_label} · {area}</div><h1>{tagline}</h1>
<p class="lede">{lede}</p>{rating}<div class="ctas"><a class="btn" href="tel:{tel}">Call now</a><a class="btn ghost" href="#book">Book or get a quote</a></div></div></div>
<section><div class="wrap"><h2>What we do</h2><div class="svc">{services}</div></div></section>
<section id="book" style="padding-top:0"><div class="wrap"><div class="missed"><h3>Missed our call? We'll text you straight back.</h3>
<p>Busy with a customer? Leave your number and you'll get a text within minutes, so you're never left waiting.</p>
<form onsubmit="this.innerHTML='<p><b>Thanks, we&rsquo;ll text you back shortly.</b></p>';return false"><input type="tel" placeholder="Your mobile number" required><button class="btn" type="submit">Text me back</button></form></div></div></section>
<section style="padding-top:0"><div class="wrap"><h2>Why {area} picks us</h2><div class="why">
<div><b>Local to {area}</b>Quick to get to you, and we know the area.</div>
<div><b>{proof_title}</b>{proof}</div>
<div><b>Easy to book</b>Call, text or leave your number and we'll come back to you fast.</div></div></div></section>
<footer><div class="wrap"><div class="logo">{name}</div><div>{address}</div><div><a href="tel:{tel}">{phone}</a></div></div></footer>
<div class="bar"><a class="btn" href="tel:{tel}">Call</a><a class="btn ghost" href="#book">Text me back</a></div>
</body></html>"""

def page(l, hero_base):
    c = trades.get(l.get("trade")); bg, ink, acc, soft = c["palette"]; e = lambda s: html.escape(str(s or ""))
    area = l.get("area") or "your area"; tr = (l.get("trade") or "").strip()
    hero = f"{hero_base}/hero-{(tr if tr in trades.T else 'default').replace(' ', '-')}.jpg"
    rv = int(l.get("reviews") or 0); rt = float(l.get("rating") or 0)
    rating = f'<div class="rate"><b>{stars(rt)}</b> {rt:.1f} from {rv} Google reviews</div>' if rv >= 5 and rt >= 4.0 else ""
    proof_title, proof = (f"Rated {rt:.1f} on Google", f"{rv} reviews from real customers.") if rating else ("Friendly and reliable", "Turn up when we say, do the job properly.")
    svc = "".join(f"<div>{e(s)}<small>Ask for a price</small></div>" for s in c["services"])
    tel = re.sub(r"[^\d+]", "", l.get("phone") or "")
    return PAGE.format(name=e(l["name"]), area=e(area), bg=bg, ink=ink, acc=acc, soft=soft, hero=hero, tel=tel,
        phone=e(nice_phone(l.get("phone"))), phone_short=e(nice_phone(l.get("phone"))), trade_label=e(tr.title() or "Local business"),
        tagline=e(c["tagline"]), lede=e(f"{l['name']} in {area}. Get in touch today for a quick, honest quote."),
        rating=rating, services=svc, proof_title=e(proof_title), proof=e(proof), address=e(l.get("address")))

if __name__ == "__main__":
    leads = json.load(open(sys.argv[1])); out = sys.argv[2]; base = sys.argv[3]; done = []
    for l in leads:
        if l["name"] == l["name"].lower(): l["name"] = l["name"].title()
    for l in leads:
        s = slug(f"{l['name']}-{l.get('area') or ''}") or str(l["id"])
        os.makedirs(os.path.join(out, s), exist_ok=True)
        open(os.path.join(out, s, "index.html"), "w").write(page(l, base)); done.append({"id": l["id"], "slug": s})
    print(json.dumps(done))
