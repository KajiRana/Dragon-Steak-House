#!/usr/bin/env python3
"""Static site generator. Reads data/dishes.json and writes every page. Run: python3 build.py"""
import json, html, pathlib

ROOT = pathlib.Path(__file__).parent
SITE = "https://dragon-steak-house.vercel.app"   # change when the custom domain is added
PHONE, PHONE_FMT = "918698564244", "+91 86985 64244"
MAPS = "https://www.google.co.in/maps/place/Dragon+Steak+House/@15.6182533,73.7348903,17z/data=!3m1!4b1!4m6!3m5!1s0x3bbfe9f9f8fcde5b:0x385e6ba110c0665b!8m2!3d15.6182481!4d73.7374652!16s%2Fg%2F11h8jy7752?entry=ttu&g_ep=EgoyMDI2MTAyMC4wIKXMDSoASAFQAw%3D%3D"
EMBED = "https://www.google.com/maps?q=15.6182481,73.7374652&z=17&hl=en&output=embed"
data = json.loads((ROOT / "data/dishes.json").read_text())
CATS, D = data["categories"], data["dishes"]
for d in D:
    d["img"] = f"assets/dishes/{d.get('img', d['slug'])}.jpg"
e = html.escape
# Hand-drawn style line illustrations, reused as section ornaments
LOGO = '<svg class="logo" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="22" fill="none" stroke="currentColor" stroke-width="1.2"/><path d="M14 30c3-9 9-14 17-14-3 2-4 4-4 6 3-1 6 0 8 2-3 0-5 1-6 3 2 1 3 3 3 5-3-2-6-3-10-2-3 0-6 1-8 0z" fill="currentColor"/><path d="M22 12c1 2 0 4-1 5 2 0 3-1 4-3 0 2 1 3 2 4" fill="none" stroke="#b4532a" stroke-width="1.4" stroke-linecap="round"/></svg>'
WAVE = '<svg class="orn" viewBox="0 0 220 24" aria-hidden="true"><path d="M2 12c18-10 36-10 54 0s36 10 54 0 36-10 54 0 36 10 54 0" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>'
PALM = '<svg class="ill palm" viewBox="0 0 120 160" aria-hidden="true"><path d="M62 158c-4-40-2-80 6-112" fill="none" stroke="currentColor" stroke-width="2"/><path d="M68 46c-18-18-42-18-60-6 20-2 36 2 48 12M68 46c4-22 22-38 46-38-16 8-28 20-34 34M68 46c22-10 42-4 50 10-16-8-32-8-44-2M68 46c-6-18-22-30-40-30 14 6 24 16 30 28M68 46c-20 2-34 14-38 30 10-12 22-20 34-22" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'
FLAME = '<svg class="ill flame" viewBox="0 0 60 80" aria-hidden="true"><path d="M30 76c-16 0-24-12-22-26 2-12 12-16 12-30 8 6 10 14 8 22 4-2 6-6 6-10 8 8 14 18 12 28-2 10-8 16-16 16z" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M30 76c-6 0-10-6-8-12 1-5 6-7 6-13 5 4 9 10 8 16-1 6-3 9-6 9z" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>'
ANALYTICS = '<script defer src="/_vercel/insights/script.js"></script>'
NAV = [("home", "index.html", "Home"), ("menu", "menu.html", "Menu"), ("offers", "offers.html", "Offers"), ("gallery", "gallery.html", "Gallery"), ("events", "events.html", "Events"), ("about", "about.html", "Our Story"), ("visit", "visit.html", "Visit &amp; Delivery")]
inr = lambda n: f"₹{n:,}"
by = {d["slug"]: d for d in D}

def head(title, desc, p, extra=""):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:image" content="{SITE}/assets/gallery/deck.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="icon" href="{p}assets/logo.svg" type="image/svg+xml"><meta name="theme-color" content="#fbf7f0">
<link rel="stylesheet" href="{p}style.css">{ANALYTICS}{extra}</head><body data-base="{p}">"""

def header(p, on=""):
    a = lambda k, href, t: f'<a href="{p}{href}"{" class=on" if on == k else ""}>{t}</a>'
    return f"""<header class="hdr"><div class="wrap">
<a class="brand" href="{p}index.html">{LOGO}<span><b>Dragon <i>Steak</i> House</b><small>Bar &amp; Restaurant · Morjim</small></span></a>
<nav class="nav">{"".join(a(*n) for n in NAV)}</nav>
<div class="tools"><a class="lang" href="{p}menu-ru.html" lang="ru" title="Меню на русском">RU</a><button class="cartb" data-opencart aria-label="Open order"><span>Order</span><b data-cartcount>0</b></button><button class="burger" aria-label="Menu"><i></i><i></i></button></div></div></header>"""

def footer(p):
    return f"""<footer class="ft"><div class="wrap"><div class="cols">
<div><a class="brand" href="{p}index.html"><b>Dragon Steak House</b><small>Bar &amp; Restaurant · Morjim</small></a>
<p style="margin-top:16px;font-size:.92rem;max-width:300px">Steaks, Goan seafood and Thai kitchen on Morjim beach. Dine upstairs by the river, or have it brought to you.</p></div>
<div><h5>Explore</h5>{"".join(f'<a href="{p}{h}">{t}</a>' for _, h, t in NAV[1:])}<a href="{p}menu-ru.html" lang="ru">Меню на русском</a></div>
<div><h5>Popular</h5>{"".join(f'<a href="{p}dishes/{s}.html">{e(by[s]["name"])}</a>' for s in ("couples-feast", "king-fish-rava-fry", "fire-grilled-steak", "spinach-momos", "full-english-breakfast"))}</div>
<div><h5>Find us</h5><a href="{MAPS}" target="_blank" rel="noopener">Temb Vaddo, beach,<br>Morjim, Goa 403512</a><a href="tel:+{PHONE}">{PHONE_FMT}</a><a href="https://wa.me/{PHONE}" target="_blank" rel="noopener">WhatsApp</a><a href="https://t.me/+{PHONE}" target="_blank" rel="noopener">Telegram</a><a>Open daily 7 am – 11 pm</a></div>
</div><div class="copy"><span>© <span id="yr"></span> Dragon Steak House, Morjim, Goa</span><span>Dish photography is illustrative (Unsplash).</span></div></div></footer>
<script src="{p}menu.js"></script><script src="{p}cart.js"></script><script>document.getElementById("yr").textContent=new Date().getFullYear()</script></body></html>"""

def card(d, p, delay=""):
    nv = "" if d["veg"] else " nv"
    tag = f'<span class="tag">{e(d["tag"])}</span>' if d["tag"] else ""
    tw = '<span class="tw" title="Holds up well for delivery">🛵 Travels well</span>' if d.get("travels") else ""
    return f"""<article class="dish reveal {delay}"><div class="ph"><img loading="lazy" src="{p}{d["img"]}" alt="{e(d["name"])}">{tag}{tw}</div>
<div class="bd"><h3><a href="{p}dishes/{d["slug"]}.html">{e(d["name"])}</a><span class="price">{inr(d["price"])}</span></h3>
<p><i class="dot{nv}"></i>{e(d["short"])}</p><div class="row"><span style="font-size:.8rem;color:var(--mute)">{e(d["prep"])}</span><span data-qty="{d["slug"]}"></span></div></div></article>"""

def phead(eyebrow, title, lead=""):
    l = f'<p class="lead" style="margin:16px auto 0">{lead}</p>' if lead else ""
    return f'<div class="phead"><div class="wrap"><span class="eyebrow">{eyebrow}</span><h1 class="split-words">{title}</h1>{l}<div class="orn-wrap">{WAVE}</div></div></div>'

def write(path, content):
    f = ROOT / path; f.parent.mkdir(parents=True, exist_ok=True); f.write_text(content)

# ---------- menu.js (consumed by cart.js)
write("menu.js", "// GENERATED by build.py from data/dishes.json. Do not edit.\nconst DISHES = " +
      json.dumps([{k: d[k] for k in ("slug", "name", "price", "img", "cat")} for d in D], ensure_ascii=False) + ";\n")
write("assets/logo.svg", LOGO.replace('class="logo" ', 'xmlns="http://www.w3.org/2000/svg" ').replace("currentColor", "#27302f"))

# ---------- home
sig = [by[s] for s in ("king-fish-rava-fry", "fire-grilled-steak", "spinach-momos", "seafood-pasta", "red-thai-curry", "king-fish-fillet")]
rib = "".join(f"<span>{t}</span>" for t in ("Free delivery over ₹1000", "Open daily 7 am – 11 pm", "We deliver anywhere", "Pay by UPI or Google Pay", "Steaks · Seafood · Thai", "Morjim Beach, Goa")) * 2
ld = json.dumps({"@context": "https://schema.org", "@type": "Restaurant", "name": "Dragon Steak House", "image": [f"{SITE}/assets/gallery/deck.jpg", f"{SITE}/assets/gallery/storefront.jpg", f"{SITE}/assets/gallery/bar.jpg"], "servesCuisine": ["Steak", "Seafood", "Thai", "Goan"], "priceRange": "₹₹", "telephone": f"+{PHONE}", "url": SITE, "hasMenu": f"{SITE}/menu.html", "acceptsReservations": True,
    "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.4", "bestRating": "5", "ratingCount": "78"},
    "address": {"@type": "PostalAddress", "streetAddress": "Temb Vaddo, beach", "addressLocality": "Morjim", "addressRegion": "Goa", "postalCode": "403512", "addressCountry": "IN"},
    "geo": {"@type": "GeoCoordinates", "latitude": 15.6182481, "longitude": 73.7374652}, "openingHours": "Mo-Su 07:00-23:00", "hasMap": MAPS})
home = head("Dragon Steak House | Steaks, Goan Seafood & Thai in Morjim", "Dragon Steak House on Morjim beach, Goa. Fire-grilled steaks, King Fish rava fry, spinach momos and Thai curries. Order online, free delivery over ₹1000.", "", f'<script type="application/ld+json">{ld}</script>') + header("", "home") + f"""
<section class="hero"><div class="wrap"><div>
<span class="eyebrow">Morjim Beach · Goa</span>
<h1 class="split-words">Where the Goan coast meets the <em>open flame</em></h1>
<p class="lead">Fire-grilled steaks, kingfish rava fry, spinach momos and Thai curries, served on a laterite-stone shack by the river. Dine with us, or have it brought to wherever you are staying.</p>
<div class="cta"><a class="btn pri" href="menu.html">Order now</a><a class="btn sec" href="visit.html">Visit &amp; delivery</a></div>
<div class="proof"><div><b>4.4 ★</b>Google rating</div><div><b>7 am – 11 pm</b>Open every day</div><div><b>₹0</b>Delivery over ₹1000</div></div></div>
<div class="arch"><div class="main"><img src="assets/gallery/deck.jpg" alt="Thatched upstairs dining deck at Dragon Steak House with prayer flags, palms and wicker chairs"></div>
<div class="float f1"><img src="assets/dishes/fire-grilled-steak.jpg" alt=""><i class="smoke"></i><i class="smoke s2"></i><i class="smoke s3"></i></div><div class="float f2"><img src="assets/dishes/spinach-momos.jpg" alt=""></div>
<div class="seal"><div><b>7–11</b>open daily</div></div></div></div>{PALM}</section>
<div class="ribbon"><div>{rib}</div></div>
<section class="bfast" data-when="breakfast" hidden><div class="wrap"><div class="bf-in"><div><span class="eyebrow">Good morning, Morjim</span><h2>Breakfast is served until 11 am</h2><p class="lead">Full breakfast platters, banana pancakes and fluffy omelettes, delivered to your villa while the coffee is still hot.</p><a class="btn pri" href="menu.html#Breakfast" style="margin-top:22px">Order breakfast</a></div>
<div class="grid g2">{"".join(card(by[s], "", f"d{i+1}") for i, s in enumerate(("full-english-breakfast", "banana-pancakes")))}</div></div></div></section>
<section class="combos"><div class="wrap"><div class="center"><span class="eyebrow">Feasts &amp; combos</span><h2>More food, better value, free delivery</h2><p class="lead">Set meals built for couples, families and villa groups. Save on the a la carte price.</p><div class="orn-wrap">{WAVE}</div></div>
<div class="grid g3" style="margin-top:40px">{"".join(card(d, "", f"d{i+1}") for i, d in enumerate(x for x in D if x["cat"] == "Combos"))}</div></div></section>
<section><div class="wrap"><div class="center"><span class="eyebrow">Signature dishes</span><h2>Plates our guests return for</h2><p class="lead">From the chalkboard at the door to your table. Each dish has its own page with ingredients, spice level and pairing.</p></div>
<div class="grid g3" style="margin-top:50px">{"".join(card(d, "", f"d{i%3+1}") for i, d in enumerate(sig))}</div>
<div class="center" style="margin-top:44px"><a class="btn sec" href="menu.html">View the full menu</a></div></div></section>
<section class="sand"><div class="wrap split"><div class="frame reveal"><img loading="lazy" src="assets/dishes/grilled-fish-lime.jpg" alt="Grilled fish with lime"></div>
<div class="reveal d1"><span class="eyebrow">Our kitchen</span><h2>Simple technique. Fresh catch. Serious fire.</h2>
<p class="lead">We cook what the coast gives us. Kingfish in a crisp rava crust, coconut curries sharpened with kokum, steaks seared over open flame and momos steamed fresh. Upstairs the tables look over the river, downstairs the breeze comes straight from the beach.</p>
<div class="stat"><div><b data-count="4.4">4.4</b>on Google</div><div><b data-count="{len(D)}">{len(D)}</b>dishes &amp; feasts</div><div><b>7 am</b>to 11 pm daily</div></div>
<a class="btn pri" style="margin-top:34px" href="about.html">Read our story</a></div></div></section>
<section><div class="wrap"><div class="center"><span class="eyebrow">Delivered to you</span><h2>Beach-side dining, wherever you stay</h2><p class="lead">Order directly from us. No commissions, no middlemen, just a quicker, fresher meal at your door.</p></div>
<div class="steps"><div class="step reveal"><h3>Choose</h3><p>Browse the menu and add dishes to your order.</p></div><div class="step reveal d1"><h3>Send</h3><p>Share your address or pin, order now or schedule for later. We confirm on WhatsApp or Telegram, with the delivery fee for your distance.</p></div><div class="step reveal d2"><h3>Pay and enjoy</h3><p>Pay by UPI, Google Pay or cash. Free delivery over ₹1000, just ₹50 below within our local zone.</p></div></div>
<div class="chips"><span class="chip">Guests praise the momos</span><span class="chip">Friendly, attentive service</span><span class="chip">River-view upstairs seating</span><span class="chip">Fair prices</span><span class="chip">Takeaway &amp; delivery</span></div></div></section>
<section class="sand"><div class="wrap center"><span class="eyebrow">Plan your visit</span><h2>Temb Vaddo, Morjim Beach</h2><p class="lead" style="margin-bottom:30px">Open every day from 7 am to 11 pm. Ground-floor and upstairs seating.</p>
<div class="cta" style="justify-content:center;margin:0"><a class="btn pri" href="{MAPS}" target="_blank" rel="noopener">Get directions</a><a class="btn sec" href="tel:+{PHONE}">Call {PHONE_FMT}</a></div></div></section>
""" + footer("")
write("index.html", home)

# ---------- menu
tabs = '<button class="on" data-cat="all">All</button>' + "".join(f'<button data-cat="{e(c)}">{e(c)}</button>' for c in CATS)
sections = "".join(f'<div class="cat" data-cat="{e(c)}"><h2 class="serif reveal">{e(c)}</h2><div class="grid g3">{"".join(card(d, "", f"d{i%3+1}") for i, d in enumerate(D) if d["cat"] == c)}</div></div>' for c in CATS if any(d["cat"] == c for d in D))
write("menu.html", head("Menu | Dragon Steak House, Morjim", "Steaks, Goan seafood, Thai curries, momos and pasta at Dragon Steak House, Morjim. Order online for delivery.", "") + header("", "menu") + f"""
{phead("The menu", "From the grill, the sea and the wok", "Tap any dish for the full story. Free delivery over ₹1000. 🛵 marks dishes that travel especially well.")}
<section style="padding-top:30px"><div class="wrap"><div class="tabs">{tabs}</div>{sections}</div></section>""" + footer(""))

# ---------- dish pages
for d in D:
    p = "../"
    sp = f'<span class="spice">{"●" * d["spice"]}<i>{"●" * (3 - d["spice"])}</i></span>' if d["spice"] else "None"
    rel = [x for x in D if x["cat"] == d["cat"] and x["slug"] != d["slug"]] or [x for x in D if x["slug"] != d["slug"]]
    rel = (rel + [x for x in D if x not in rel and x["slug"] != d["slug"]])[:3]
    nv = "" if d["veg"] else " nv"
    ld = json.dumps({"@context": "https://schema.org", "@type": "MenuItem", "name": d["name"], "description": d["short"], "image": f"{SITE}/{d['img']}",
                     "offers": {"@type": "Offer", "price": d["price"], "priceCurrency": "INR"}, **({"suitableForDiet": "https://schema.org/VegetarianDiet"} if d["veg"] else {})})
    allerg = "".join(f"<span>{e(a)}</span>" for a in d["allergens"]) or "<span>None of the major allergens</span>"
    write(f"dishes/{d['slug']}.html", head(f"{d['name']} | Dragon Steak House, Morjim", d["short"], p, f'<script type="application/ld+json">{ld}</script>') + header(p, "menu") + f"""
<div class="wrap"><div class="dtop"><div class="dphoto reveal"><img src="{p}{d["img"]}" alt="{e(d["name"])}"></div>
<div class="dinfo reveal d1"><div class="crumb"><a href="{p}index.html">Home</a> / <a href="{p}menu.html">Menu</a> / {e(d["cat"])}</div>
<span class="eyebrow">{e(d["tag"] or d["cat"])}</span><h1>{e(d["name"])}</h1><p class="ru" lang="ru">{e(d["ru"])}</p><div class="dprice"><i class="dot{nv}"></i>{inr(d["price"])}</div>
<p class="lead">{e(d["long"])}</p>
<div class="meta"><div>Spice level<b>{sp}</b></div><div>Serves<b>{e(d["serves"])}</b></div><div>Prepared in<b>{e(d["prep"])}</b></div></div>
<p class="tw-note">{"🛵 Travels well: packed to arrive hot and intact." if d.get("travels") else "🍽 Best enjoyed fresh at the restaurant. Delivery is available, but it is at its best on the plate."}</p>
<h4>What goes in</h4><div class="tags">{"".join(f"<span>{e(i)}</span>" for i in d["ingredients"])}</div>
<h4>Allergen information</h4><div class="tags">{allerg}</div>
<h4>Best paired with</h4><p style="color:var(--mute)">{e(d["pairing"])}</p>
<div class="buy"><span data-qty="{d["slug"]}"></span><a class="btn sec" href="{p}menu.html">Back to menu</a></div>
<p class="note">Free delivery over ₹1000, ₹50 below within our local zone. Distance-based fee confirmed on chat for farther addresses. Photo is illustrative.</p></div></div></div>
<section><div class="wrap"><div class="center"><span class="eyebrow">Pairs well</span><h2>You may also like</h2></div><div class="grid g3" style="margin-top:44px">{"".join(card(x, p, f"d{i+1}") for i, x in enumerate(rel))}</div></div></section>""" + footer(p))

# ---------- about
write("about.html", head("Our Story | Dragon Steak House, Morjim", "A laterite-stone shack on Morjim beach serving steaks, Goan seafood and Thai food by the river.", "") + header("", "about") + f"""
{phead("Our story", "A shack, a flame and the Goan coast")}
<section style="padding-top:30px"><div class="wrap split"><div class="frame reveal"><img src="assets/gallery/bar.jpg" alt="The bar at Dragon Steak House under its tiled roof, with palms in front"></div>
<div class="reveal d1"><h2>Red laterite, thatch and a chalkboard that changes daily</h2>
<p class="lead">Dragon Steak House stands at Temb Vaddo on Morjim beach, a few steps from the river. The pillars are local laterite, the roof is thatch, and the menu is written fresh each day.</p>
<p class="lead" style="margin-top:16px">Our idea is simple: cook good food over real fire, lean on the local catch, and welcome everyone like a neighbour. Steaks share the board with Goan fish curry, momos and Thai curries because that is how our guests, travellers and locals alike, like to eat.</p></div></div></section>
<section class="sand"><div class="wrap"><div class="center"><span class="eyebrow">What we believe</span><h2>Three simple promises</h2></div>
<div class="steps"><div class="step reveal"><h3>Fresh first</h3><p>Seafood and daily specials, chalked on the board at the door.</p></div><div class="step reveal d1"><h3>Fire and care</h3><p>Steaks seared over open flame, curries simmered slow, momos steamed fresh.</p></div><div class="step reveal d2"><h3>Warm welcome</h3><p>Friendly service, fair prices and a table with a view, upstairs or down.</p></div></div></div></section>
<section><div class="wrap center"><h2>Come hungry</h2><p class="lead" style="margin-bottom:28px">Reserve by message, or order to your door.</p><div class="cta" style="justify-content:center;margin:0"><a class="btn pri" href="menu.html">See the menu</a><a class="btn sec" href="https://wa.me/{PHONE}" target="_blank" rel="noopener">Message us</a></div></div></section>""" + footer(""))

book_form = f"""<form class="co book" data-wa="Table / event enquiry"><div class="grid g2"><input name="Name" placeholder="Your name" required><input name="Phone" type="tel" placeholder="Phone number" required></div>
<div class="grid g2"><input name="Date" type="date" required><input name="Time" type="time" required></div>
<div class="grid g2"><input name="Guests" type="number" min="1" max="80" placeholder="Number of guests" required><select name="Occasion"><option>Dinner</option><option>Birthday</option><option>Anniversary</option><option>Group / villa party</option><option>Breakfast</option></select></div>
<textarea name="Notes" rows="3" placeholder="Seating preference (upstairs river view or ground floor), food preferences, cake, decorations..."></textarea>
<button class="btn pri block" type="submit">Send enquiry on WhatsApp</button></form>"""

# ---------- visit
faqs = [("Do you deliver everywhere?", "Yes, there is no distance limit. Delivery is free on orders of ₹1000 or more and ₹50 below that within our local zone. For farther addresses we confirm the fee by distance on WhatsApp or Telegram before you pay."),
        ("How do I pay?", "UPI or Google Pay to kajirana94@oksbi, or cash on delivery. The order summary includes a payment link."),
        ("What are your hours?", "Every day from 7 am to 11 pm."),
        ("Can I reserve a table?", "Message us on WhatsApp with your date, time and group size. We seat guests on the ground floor and upstairs by the river."),
        ("Can I order when you are closed?", "Yes. Choose \"Schedule for later\" at checkout and pick a time. We confirm your pre-order as soon as we open at 7 am."),
        ("Is there vegetarian food?", "Yes. Spinach Momos, Veg Thai Curry, Banana Pancakes, the Veggie Feast and more are vegetarian, and every dish page shows allergens.")]
write("visit.html", head("Visit & Delivery | Dragon Steak House, Morjim", "Temb Vaddo beach, Morjim, Goa 403512. Open 7 am to 11 pm. Free delivery over ₹1000. Call, WhatsApp or Telegram +91 86985 64244.", "") + header("", "visit") + f"""
{phead("Visit &amp; delivery", "Find us, or let us find you")}
<section style="padding-top:30px"><div class="wrap split"><div class="frame reveal"><img src="assets/gallery/storefront.jpg" alt="Front of Dragon Steak House at Temb Vaddo, with the white wood-fired oven by the gate"></div>
<div class="reveal d1"><span class="eyebrow">Spot us from the road</span><h2>Look for the white wood-fired oven</h2><p class="lead">Two floors with striped pillars at Temb Vaddo, Morjim. Our dome oven sits by the front gate, and the thatched deck is upstairs.</p></div></div></section>
<section style="padding-top:30px"><div class="wrap"><div class="cards">
<div class="card reveal"><h3>Address</h3><p>Temb Vaddo, beach,<br>Morjim, Goa 403512</p><br><a href="{MAPS}" target="_blank" rel="noopener">Open in Google Maps →</a></div>
<div class="card reveal d1"><h3>Hours</h3><p>Every day<br>7:00 am – 11:00 pm</p></div>
<div class="card reveal d2"><h3>Order direct</h3><p>{PHONE_FMT}</p><br><a href="tel:+{PHONE}">Call</a> · <a href="https://wa.me/{PHONE}" target="_blank" rel="noopener">WhatsApp</a> · <a href="https://t.me/+{PHONE}" target="_blank" rel="noopener">Telegram</a></div></div>
<div style="margin-top:36px"><iframe class="map" loading="lazy" title="Dragon Steak House on Google Maps" src="{EMBED}" referrerpolicy="no-referrer-when-downgrade"></iframe></div></div></section>
<section class="sand"><div class="wrap split"><div><span class="eyebrow">Delivery</span><h2>Free over ₹1000. ₹50 below.</h2><p class="lead">We deliver anywhere you are. The ₹50 fee applies within our local zone. For farther addresses we confirm the fee by distance, in chat, before you pay. Add a little more to your order and the bar in your cart shows when delivery turns free.</p><div class="cta" style="margin-top:26px"><a class="btn pri" href="menu.html">Start an order</a></div></div>
<div class="faq">{"".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faqs)}</div></div></section>
<section><div class="wrap split"><div><span class="eyebrow">Book a table</span><h2>Reserve upstairs by the river</h2><p class="lead">Send your date, time and group size. We confirm on WhatsApp.</p></div><div>{book_form}</div></div></section>""" + footer(""))

# ---------- offers (owner: edit freely; the welcome discount and loyalty rules are enforced in cart.js CONFIG)
OFFERS = [("Welcome offer", "₹50 off", "Your first direct order of ₹500 or more gets ₹50 off, applied automatically in the cart.", "menu.html", "Start your first order"),
          ("Free delivery", "₹0 delivery", "Every order of ₹1000 or more is delivered free. Below that it is ₹50 in our local zone.", "menu.html", "Build your order"),
          ("Loyalty", "6th order treat", "Every 6th direct order comes with a free Fresh Lime Soda. We keep count for you.", "menu.html", "Order again"),
          ("Feasts", "Save up to ₹241", "Couple's Feast, Family Seafood Feast and Veggie Feast cost less than ordering a la carte.", "menu.html#Combos", "See the feasts"),
          ("Breakfast delivery", "From 7 am", "Full breakfast, pancakes and omelettes delivered to your villa until 11 am.", "menu.html#Breakfast", "Order breakfast"),
          ("Celebrations", "Groups welcome", "Birthdays and group dinners upstairs by the river. Message us to plan the table and menu.", "events.html", "Plan an event")]
write("offers.html", head("Offers | Dragon Steak House, Morjim", "Welcome discount, free delivery over ₹1000, loyalty treats and feast combos at Dragon Steak House, Morjim.", "") + header("", "offers") + phead("Offers", "Good food, even better value", "Order direct from our website for the best prices. No app commissions means more for you.") + f"""
<section style="padding-top:30px"><div class="wrap"><div class="grid g3">{"".join(f'<div class="offer reveal d{i%3+1}"><span class="eyebrow">{e(t)}</span><h3>{e(big)}</h3><p>{e(txt)}</p><a class="btn sec sm" href="{h}">{e(cta)}</a></div>' for i, (t, big, txt, h, cta) in enumerate(OFFERS))}</div>
<p class="note center" style="margin-top:30px">Offers apply to direct orders on this website, WhatsApp and Telegram. One welcome offer per customer. We may update offers at any time.</p></div></section>""" + footer(""))

# ---------- gallery
GAL = [("assets/gallery/deck.jpg", "Our thatched upstairs deck", "wide"), ("assets/dishes/lobster-thermidor.jpg", "Lobster, the way we plate it", ""), ("assets/gallery/fresh-lobster.jpg", "Fresh lobster from the boats", ""),
       ("assets/gallery/dining-room.jpg", "Ground-floor dining and bar", "tall"), ("assets/gallery/bar.jpg", "The bar", ""), ("assets/gallery/fresh-catch.jpg", "Today's catch on ice", ""),
       ("assets/gallery/deck-trees.jpg", "Tables among the trees", "wide"), ("assets/gallery/pizza-oven.jpg", "Our wood-fired oven", "tall"), ("assets/gallery/storefront.jpg", "Find us at Temb Vaddo", ""),
       ("assets/gallery/staircase.jpg", "Up to the deck", ""), ("assets/dishes/fire-grilled-steak.jpg", "Steak over open flame", ""), ("assets/dishes/spinach-momos.jpg", "Spinach momos", ""),
       ("assets/dishes/king-fish-rava-fry.jpg", "King Fish Rava Fry", ""), ("assets/dishes/pepper-steak-platter.jpg", "Pepper steak platter", ""), ("assets/dishes/red-thai-curry.jpg", "Red Thai curry", "")]
write("gallery.html", head("Gallery | Dragon Steak House, Morjim", "Photos of Dragon Steak House, our dishes and Morjim beach.", "") + header("", "gallery") + phead("Gallery", "Fire, food and the Goan coast") + f"""
<section style="padding-top:30px"><div class="wrap"><div class="gal">{"".join(f'<figure class="reveal {c}" data-lightbox><img loading="lazy" src="{s}" alt="{e(t)}"><figcaption>{e(t)}</figcaption></figure>' for s, t, c in GAL)}</div>
<p class="note center" style="margin-top:24px">Restaurant, lobster and fresh-catch photos are our own. Other dish photos are illustrative while we shoot our own.</p></div></section>""" + footer(""))

# ---------- events / table booking (WhatsApp enquiry)
write("events.html", head("Events & Private Dining | Dragon Steak House, Morjim", "Birthdays, group dinners and celebrations upstairs by the river at Dragon Steak House, Morjim.", "") + header("", "events") + phead("Events &amp; tables", "Celebrate by the river", "Birthdays, anniversaries and villa-group dinners, with set menus and upstairs river-view seating.") + f"""
<section style="padding-top:30px"><div class="wrap split"><div class="frame reveal"><img loading="lazy" src="assets/gallery/deck-trees.jpg" alt="Upstairs deck tables surrounded by trees"></div>
<div class="reveal d1"><span class="eyebrow">Plan with us</span><h2>Tell us the date. We will handle the feast.</h2>
<ul class="ticks"><li>Upstairs river-view tables or ground floor for easy access</li><li>Group set menus built from our feasts</li><li>Birthdays and anniversaries, bring your cake or ask us</li><li>Delivery feasts for villa parties</li></ul>{book_form}</div></div></section>""" + footer(""))

# ---------- Russian menu
RU_CAT = {"Breakfast": "Завтраки", "Combos": "Сеты", "Seafood": "Морепродукты", "Steaks & Grill": "Стейки и гриль", "Thai & Asian": "Тайская и азиатская кухня", "Pasta": "Паста", "Desserts": "Десерты", "Drinks": "Напитки"}
ru_rows = "".join(f'<div class="cat"><h2 class="serif">{RU_CAT[c]} <small>{e(c)}</small></h2><div class="rulist">' + "".join(
    f'<div class="rurow"><img loading="lazy" src="{d["img"]}" alt=""><div><a href="dishes/{d["slug"]}.html"><b>{e(d["ru"])}</b></a><small>{e(d["name"])}{" · вегетарианское" if d["veg"] else ""}</small></div><span class="price">{inr(d["price"])}</span><span data-qty="{d["slug"]}"></span></div>' for d in D if d["cat"] == c) + "</div></div>" for c in CATS)
write("menu-ru.html", head("Меню | Dragon Steak House, Морджим, Гоа", "Стейки, морепродукты, тайская кухня и завтраки. Бесплатная доставка от ₹1000. Морджим, Гоа.", "").replace('<html lang="en">', '<html lang="ru">') + header("", "menu") + phead("Меню", "Стейки, морепродукты и тайская кухня", "Бесплатная доставка при заказе от ₹1000, ниже — ₹50. Доставляем куда угодно. Заказ через WhatsApp или Telegram, оплата UPI / Google Pay или наличными.") + f"""
<section style="padding-top:30px"><div class="wrap">{ru_rows}</div></section>""" + footer(""))

# ---------- partner QR kit (for villas / guesthouses; not indexed)
write("partners.html", head("Partner QR kit | Dragon Steak House", "Printable QR menu cards for partner villas and guesthouses.", "", '<meta name="robots" content="noindex"><script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>') + header("", "") + phead("Partners", "QR menu cards for villas &amp; stays", "Type the property name, print the card and place it in rooms. Orders from that card are tagged with the property so you can reward partners.") + f"""
<section style="padding-top:30px"><div class="wrap"><div class="qrtool"><input id="prop" placeholder="Property name, e.g. Palm Villa Ashwem"><button class="btn pri" id="mk">Create card</button><button class="btn sec" onclick="print()">Print</button></div>
<div class="qrcard" id="card"><div class="brand">{LOGO}<span><b>Dragon <i>Steak</i> House</b><small>Bar &amp; Restaurant · Morjim</small></span></div>
<h3>Hungry? Scan to order.</h3><div id="qr"></div><p>Steaks · Goan seafood · Thai · Breakfast from 7 am<br><b>Free delivery over ₹1000</b> · ₹50 off your first order</p><p class="small" id="for"></p><p class="small">WhatsApp {PHONE_FMT}</p></div></div></section>
<script>
const mk=()=>{{const n=document.getElementById("prop").value.trim()||"guest";const slug=n.toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"");
const q=document.getElementById("qr");q.innerHTML="";new QRCode(q,{{text:"{SITE}/?ref="+slug,width:180,height:180,colorDark:"#27302f",colorLight:"#ffffff"}});document.getElementById("for").textContent="Made for "+n;}};
document.getElementById("mk").onclick=mk;addEventListener("load",mk);</script>""" + footer(""))

# ---------- 404, robots, sitemap, vercel
write("404.html", head("Page not found | Dragon Steak House", "Page not found", "/") + header("/") + """<div class="phead"><div class="wrap"><h1>This plate is not on the menu</h1><p class="lead" style="margin:18px auto 28px">Let us take you back to something delicious.</p><a class="btn pri" href="/menu.html">View menu</a></div></div>""" + footer("/"))
urls = ["", "menu.html", "offers.html", "gallery.html", "events.html", "about.html", "visit.html", "menu-ru.html"] + [f"dishes/{d['slug']}.html" for d in D]
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{SITE}/{u}</loc></url>" for u in urls) + "</urlset>")
write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
print(f"Built {len(urls)+1} pages")
