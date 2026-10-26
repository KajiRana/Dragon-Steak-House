// Shared by every page: cart drawer, offers, delivery, checkout, nav and animations.
const CONFIG = {
  PHONE: "918698564244",
  UPI_ID: "kajirana94@oksbi",
  PAYEE: "Dragon Steak House",
  FREE_OVER: 1000,      // food subtotal at or above this ships free
  FEE: 50,              // local-zone fee below the threshold
  LOCAL_KM: 5,          // beyond this the fee is quoted by distance on chat
  LAT: 15.6182481, LNG: 73.7374652,
  OPEN: 7, CLOSE: 23, BREAKFAST_UNTIL: 11,   // IST hours
  WELCOME_MIN: 500, WELCOME_OFF: 50,         // first direct order discount
  LOYALTY_EVERY: 6,                          // every Nth order gets a free lime soda
};
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const inr = n => "₹" + n.toLocaleString("en-IN");
const BASE = document.body.dataset.base || "";
const dishes = Object.fromEntries(DISHES.map(d => [d.slug, d]));
const store = { get: (k, d) => { try { return JSON.parse(localStorage.getItem(k)) ?? d; } catch (e) { return d; } }, set: (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} } };
const track = (name, data) => { try { window.va && window.va("event", { name, data }); } catch (e) {} };
let cart = store.get("dsh-cart2", {}), loc = null, km = null;
const orders = store.get("dsh-orders", 0);
for (const k in cart) if (!dishes[k]) delete cart[k];

// Partner referral from QR cards: ?ref=palm-villa
const ref = new URLSearchParams(location.search).get("ref");
if (ref) store.set("dsh-ref", ref.slice(0, 60));

const istHour = () => +new Date().toLocaleString("en-US", { timeZone: "Asia/Kolkata", hour: "numeric", hour12: false }) % 24;
const isOpen = () => { const h = istHour(); return h >= CONFIG.OPEN && h < CONFIG.CLOSE; };
const subtotal = () => Object.entries(cart).reduce((s, [k, q]) => s + dishes[k].price * q, 0);
const count = () => Object.values(cart).reduce((a, b) => a + b, 0);
const feeFor = s => (s === 0 || s >= CONFIG.FREE_OVER ? 0 : CONFIG.FEE);
const discount = s => (orders === 0 && s >= CONFIG.WELCOME_MIN ? CONFIG.WELCOME_OFF : 0);
const loyaltyTreat = () => (orders + 1) % CONFIG.LOYALTY_EVERY === 0;
const total = () => { const s = subtotal(); return s + feeFor(s) - discount(s); };

document.body.insertAdjacentHTML("beforeend", `
<div class="scrim" id="scrim"></div>
<aside class="drawer" id="drawer" aria-label="Your order">
  <div class="dh"><h3>Your order</h3><button id="closeCart" aria-label="Close">✕</button></div>
  <div class="ship"><div id="shipTxt"></div><div class="bar"><i id="shipBar"></i></div></div>
  <div id="lines"></div><div id="upsell"></div><div class="sum" id="sum"></div>
  <form class="co" id="co">
    <input name="name" placeholder="Your name" required autocomplete="name">
    <input name="phone" type="tel" placeholder="Phone number" required pattern="[0-9+ ]{10,15}" autocomplete="tel">
    <textarea name="addr" rows="2" placeholder="Delivery address, villa name or landmark" required></textarea>
    <button type="button" class="btn sec sm" id="loc">📍 Share my location</button><p class="fine" id="dist"></p>
    <div class="pay"><label><input type="radio" name="when" value="now" checked> As soon as possible</label><label><input type="radio" name="when" value="later"> Schedule for later</label></div>
    <input name="at" type="datetime-local" id="at" hidden>
    <div class="pay"><label><input type="radio" name="pay" value="upi" checked> UPI / Google Pay</label><label><input type="radio" name="pay" value="cod"> Cash on delivery</label></div>
    <div class="send"><button class="btn pri block" type="submit" data-ch="wa">Send order on WhatsApp</button><button class="btn sec block" type="submit" data-ch="tg">Send order on Telegram</button><a class="btn sec block" id="upiBtn" href="#">Pay with UPI app</a></div>
    <p class="fine">We deliver anywhere. For far addresses we confirm the delivery fee by distance before you pay.</p>
  </form>
</aside>
<button class="fab" id="fab"></button><div class="toast" id="toast" role="status"></div>
<div class="lb" id="lb"><img alt=""><p></p></div>`);

function qtyHTML(slug) {
  const q = cart[slug] || 0;
  return q ? `<div class="stepper"><button data-a="-" data-s="${slug}" aria-label="Remove one">−</button><span>${q}</span><button data-a="+" data-s="${slug}" aria-label="Add one">+</button></div>`
           : `<button class="add" data-a="+" data-s="${slug}">Add to order</button>`;
}
// Suggest dishes that close the gap to free delivery, or a drink / dessert to finish
function upsell(s) {
  const inCart = k => cart[k], left = CONFIG.FREE_OVER - s;
  const pool = DISHES.filter(d => !inCart(d.slug) && d.cat !== "Combos");
  let picks = left > 0 ? pool.filter(d => d.price >= left).sort((a, b) => a.price - b.price).slice(0, 2) : [];
  if (picks.length < 2) picks = picks.concat(pool.filter(d => ["Drinks", "Desserts"].includes(d.cat) && !picks.includes(d)).slice(0, 2 - picks.length));
  if (!s || !picks.length) return "";
  return `<div class="ups"><p>${left > 0 ? "Add one of these for free delivery" : "Complete your meal"}</p>${picks.map(d =>
    `<button type="button" data-a="+" data-s="${d.slug}"><img src="${BASE}${d.img}" alt=""><span>${d.name}<b>+ ${inr(d.price)}</b></span></button>`).join("")}</div>`;
}
function update() {
  store.set("dsh-cart2", cart);
  const s = subtotal(), f = feeFor(s), dc = discount(s), n = count(), left = CONFIG.FREE_OVER - s;
  $$("[data-cartcount]").forEach(e => e.textContent = n);
  $$("[data-qty]").forEach(e => e.innerHTML = qtyHTML(e.dataset.qty));
  $("#fab").textContent = `View order · ${inr(total())}`;
  $("#fab").classList.toggle("on", n > 0 && !$("#drawer").classList.contains("on"));
  $("#shipTxt").innerHTML = s === 0 ? `Free delivery over <b>${inr(CONFIG.FREE_OVER)}</b>. ${inr(CONFIG.FEE)} below. We deliver anywhere.`
    : left > 0 ? `Add <b>${inr(left)}</b> more for <b>free delivery</b>` : `✨ You have unlocked <b>free delivery</b>`;
  $("#shipBar").style.width = Math.min(100, s / CONFIG.FREE_OVER * 100) + "%";
  $("#lines").innerHTML = n ? Object.entries(cart).map(([k, q]) => { const d = dishes[k]; return `<div class="line"><img src="${BASE}${d.img}" alt=""><div>${d.name}<small>${inr(d.price)} each</small>${qtyHTML(k)}</div><b>${inr(d.price * q)}</b></div>`; }).join("") : `<p class="empty">Your order is empty. Explore the menu and add something delicious.</p>`;
  $("#upsell").innerHTML = upsell(s);
  const perks = [];
  if (orders === 0 && s && s < CONFIG.WELCOME_MIN) perks.push(`Add ${inr(CONFIG.WELCOME_MIN - s)} more for ₹${CONFIG.WELCOME_OFF} off your first order`);
  if (loyaltyTreat() && n) perks.push("🎁 This is your loyalty order: a free Fresh Lime Soda is on us");
  $("#sum").innerHTML = n ? `<div><span>Subtotal</span><span>${inr(s)}</span></div>${dc ? `<div class="disc"><span>Welcome offer</span><span>−${inr(dc)}</span></div>` : ""}<div><span>Delivery</span><span>${f ? inr(f) : "Free"}</span></div><div class="t"><span>Total</span><span>${inr(total())}</span></div>${perks.map(p => `<p class="perk">${p}</p>`).join("")}` : "";
  $("#upiBtn").href = `upi://pay?pa=${CONFIG.UPI_ID}&pn=${encodeURIComponent(CONFIG.PAYEE)}&am=${total()}&cu=INR&tn=${encodeURIComponent("Dragon Steak House order")}`;
  $("#upiBtn").style.display = n && $("#co").pay.value === "upi" ? "" : "none";
  $("#at").hidden = $("#co").when.value !== "later";
  $("#at").required = !$("#at").hidden;
}
let toastT;
function added(k, btn) {
  const t = $("#toast"); t.textContent = `Added ${dishes[k].name}`; t.classList.add("on");
  clearTimeout(toastT); toastT = setTimeout(() => t.classList.remove("on"), 1800);
  const cb = $(".cartb"); cb.classList.remove("bump"); void cb.offsetWidth; cb.classList.add("bump");
  // Fly a dot from the button to the cart
  const a = btn.getBoundingClientRect(), b = cb.getBoundingClientRect(), dot = document.createElement("i");
  dot.className = "fly"; dot.style.left = a.left + a.width / 2 + "px"; dot.style.top = a.top + a.height / 2 + "px"; document.body.append(dot);
  requestAnimationFrame(() => { dot.style.transform = `translate(${b.left + b.width / 2 - a.left - a.width / 2}px,${b.top + b.height / 2 - a.top - a.height / 2}px) scale(.4)`; dot.style.opacity = ".2"; });
  setTimeout(() => dot.remove(), 750);
  track("add_to_cart", { dish: k });
}
document.addEventListener("click", e => {
  const b = e.target.closest("[data-a]"); if (!b) return;
  const k = b.dataset.s, d = b.dataset.a === "+" ? 1 : -1;
  cart[k] = (cart[k] || 0) + d; if (cart[k] <= 0) delete cart[k];
  update(); if (d > 0) added(k, b);
});
const open = on => { $("#drawer").classList.toggle("on", on); $("#scrim").classList.toggle("on", on); update(); if (on) track("open_cart"); };
document.addEventListener("click", e => { if (e.target.closest("[data-opencart]") || e.target.closest("#fab")) open(true); });
$("#closeCart").onclick = $("#scrim").onclick = () => open(false);
$("#co").onchange = update;
if (!isOpen()) { $("#co").when.value = "later"; $("#dist").textContent = "We are closed right now (open 7 am – 11 pm). Schedule your order and we will confirm when we open."; }

const haversine = (a, b, c, d) => { const r = x => x * Math.PI / 180, R = 6371; const h = Math.sin(r(c - a) / 2) ** 2 + Math.cos(r(a)) * Math.cos(r(c)) * Math.sin(r(d - b) / 2) ** 2; return 2 * R * Math.asin(Math.sqrt(h)); };
$("#loc").onclick = () => navigator.geolocation ? navigator.geolocation.getCurrentPosition(p => {
  const { latitude: la, longitude: lo } = p.coords;
  loc = `https://maps.google.com/?q=${la},${lo}`; km = haversine(CONFIG.LAT, CONFIG.LNG, la, lo);
  $("#loc").textContent = "📍 Location added ✓";
  $("#dist").textContent = km <= CONFIG.LOCAL_KM ? `About ${km.toFixed(1)} km away, inside our local delivery zone.` : `About ${km.toFixed(1)} km away. We will confirm the delivery fee for this distance on chat before you pay.`;
}, () => alert("Could not get your location. Please type the address.")) : alert("Location is not supported on this device.");

function message(f) {
  const s = subtotal(), fe = feeFor(s), dc = discount(s), m = ["*New order: Dragon Steak House*", ""];
  Object.entries(cart).forEach(([k, q]) => m.push(`${q} x ${dishes[k].name} = ${inr(dishes[k].price * q)}`));
  m.push("", `Subtotal: ${inr(s)}`);
  if (dc) m.push(`Welcome offer: -${inr(dc)}`);
  m.push(`Delivery: ${fe ? inr(fe) : "Free"}${km && km > CONFIG.LOCAL_KM ? ` (about ${km.toFixed(1)} km, please confirm fee)` : ""}`, `*Total: ${inr(total())}*`);
  if (loyaltyTreat()) m.push(`Loyalty: order #${orders + 1}, free Fresh Lime Soda`);
  m.push("", `Name: ${f.name.value}`, `Phone: ${f.phone.value}`, `Address: ${f.addr.value}`);
  if (loc) m.push(`Location: ${loc}`);
  m.push(`When: ${f.when.value === "later" && f.at.value ? new Date(f.at.value).toLocaleString("en-IN", { dateStyle: "medium", timeStyle: "short" }) : "As soon as possible"}`);
  const upi = f.pay.value === "upi";
  m.push(`Payment: ${upi ? "UPI / Google Pay" : "Cash on delivery"}`);
  if (upi) m.push(`UPI: upi://pay?pa=${CONFIG.UPI_ID}&pn=${encodeURIComponent(CONFIG.PAYEE)}&am=${total()}&cu=INR`);
  const r = store.get("dsh-ref", null); if (r) m.push(`Referred by: ${r}`);
  return m.join("\n");
}
$("#co").onsubmit = e => {
  e.preventDefault();
  if (!count()) return alert("Please add a dish to your order first.");
  const ch = e.submitter.dataset.ch, t = encodeURIComponent(message(e.target));
  track("send_order", { channel: ch, total: total() });
  store.set("dsh-orders", orders + 1);
  window.open(ch === "tg" ? `https://t.me/+${CONFIG.PHONE}?text=${t}` : `https://wa.me/${CONFIG.PHONE}?text=${t}`, "_blank");
};
// Table and event enquiries: any form with data-wa becomes a WhatsApp message
$$("form[data-wa]").forEach(f => f.onsubmit = e => {
  e.preventDefault();
  const lines = [`*${f.dataset.wa}: Dragon Steak House*`, ""].concat([...new FormData(f)].filter(([, v]) => v).map(([k, v]) => `${k}: ${v}`));
  track("enquiry", { type: f.dataset.wa });
  window.open(`https://wa.me/${CONFIG.PHONE}?text=${encodeURIComponent(lines.join("\n"))}`, "_blank");
});

// Menu filter tabs (also opened by #Category in the URL)
const pick = c => { $$(".tabs button").forEach(x => x.classList.toggle("on", x.dataset.cat === c)); $$(".cat").forEach(s => s.style.display = c === "all" || s.dataset.cat === c ? "" : "none"); };
$$(".tabs button").forEach(b => b.onclick = () => pick(b.dataset.cat));
const h = decodeURIComponent(location.hash.slice(1)); if (h && $(`.tabs button[data-cat="${h}"]`)) pick(h);
// Breakfast block shows only in the morning
if (istHour() < CONFIG.BREAKFAST_UNTIL) $$("[data-when=breakfast]").forEach(s => s.hidden = false);
// Gallery lightbox
$$("[data-lightbox]").forEach(f => f.onclick = () => { const lb = $("#lb"), i = $("img", f); $("img", lb).src = i.src; $("p", lb).textContent = i.alt; lb.classList.add("on"); });
$("#lb").onclick = () => $("#lb").classList.remove("on");
// Headline word-by-word reveal
$$(".split-words").forEach(h => { let i = 0; const wrap = n => { if (n.nodeType === 3) { const f = document.createDocumentFragment(); n.textContent.split(/(\s+)/).forEach(w => { if (!w.trim()) return f.append(w); const s = document.createElement("span"); s.className = "w"; s.style.animationDelay = (i++ * 0.07) + "s"; s.textContent = w; f.append(s); }); n.replaceWith(f); } else [...n.childNodes].forEach(wrap); }; [...h.childNodes].forEach(wrap); });
// Header, mobile nav, reveal, count-up
const hdr = $(".hdr"), nav = $(".nav");
addEventListener("scroll", () => hdr.classList.toggle("solid", scrollY > 30), { passive: true }); hdr.classList.toggle("solid", scrollY > 30);
$(".burger").onclick = () => nav.classList.toggle("on");
$$(".nav a").forEach(a => a.onclick = () => nav.classList.remove("on"));
const countUp = el => { const to = parseFloat(el.dataset.count), dec = (el.dataset.count.split(".")[1] || "").length, t0 = performance.now(); const step = t => { const k = Math.min(1, (t - t0) / 1200); el.textContent = (to * (1 - (1 - k) ** 3)).toFixed(dec); if (k < 1) requestAnimationFrame(step); }; requestAnimationFrame(step); };
const io = new IntersectionObserver(es => es.forEach(x => { if (!x.isIntersecting) return; x.target.classList.add("in"); $$("[data-count]", x.target).forEach(countUp); io.unobserve(x.target); }), { threshold: .1 });
$$(".reveal").forEach(el => io.observe(el));
update();
