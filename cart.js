// Shared by every page: cart drawer, delivery fee, checkout, nav, reveal animations.
const CONFIG = {
  PHONE: "918698564244",
  UPI_ID: "kajirana94@oksbi",
  PAYEE: "Dragon Steak House",
  FREE_OVER: 1000,   // food subtotal at or above this ships free
  FEE: 50,           // local-zone fee below the threshold; farther addresses are quoted by distance on chat
};
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const inr = n => "₹" + n.toLocaleString("en-IN");
const BASE = document.body.dataset.base || "";
const dishes = Object.fromEntries(DISHES.map(d => [d.slug, d]));
let cart = {}, loc = null;
try { cart = JSON.parse(localStorage.getItem("dsh-cart2") || "{}"); } catch (e) {}
for (const k in cart) if (!dishes[k]) delete cart[k];

const subtotal = () => Object.entries(cart).reduce((s, [k, q]) => s + dishes[k].price * q, 0);
const count = () => Object.values(cart).reduce((a, b) => a + b, 0);
const feeFor = s => (s === 0 || s >= CONFIG.FREE_OVER ? 0 : CONFIG.FEE);

document.body.insertAdjacentHTML("beforeend", `
<div class="scrim" id="scrim"></div>
<aside class="drawer" id="drawer" aria-label="Your order">
  <div class="dh"><h3>Your order</h3><button id="closeCart" aria-label="Close">✕</button></div>
  <div class="ship"><div id="shipTxt"></div><div class="bar"><i id="shipBar"></i></div></div>
  <div id="lines"></div><div class="sum" id="sum"></div>
  <form class="co" id="co">
    <input name="name" placeholder="Your name" required autocomplete="name">
    <input name="phone" type="tel" placeholder="Phone number" required pattern="[0-9+ ]{10,15}" autocomplete="tel">
    <textarea name="addr" rows="2" placeholder="Delivery address, villa name or landmark" required></textarea>
    <button type="button" class="btn sec sm" id="loc">📍 Share my location</button>
    <div class="pay"><label><input type="radio" name="pay" value="upi" checked> UPI / Google Pay</label><label><input type="radio" name="pay" value="cod"> Cash on delivery</label></div>
    <div class="send"><button class="btn pri block" type="submit" data-ch="wa">Send order on WhatsApp</button><button class="btn sec block" type="submit" data-ch="tg">Send order on Telegram</button><a class="btn sec block" id="upiBtn" href="#">Pay with UPI app</a></div>
    <p class="fine">We deliver anywhere. For far addresses we confirm the delivery fee by distance before you pay.</p>
  </form>
</aside>
<button class="fab" id="fab"></button>`);

function qtyHTML(slug) {
  const q = cart[slug] || 0;
  return q ? `<div class="stepper"><button data-a="-" data-s="${slug}" aria-label="Remove one">−</button><span>${q}</span><button data-a="+" data-s="${slug}" aria-label="Add one">+</button></div>`
           : `<button class="add" data-a="+" data-s="${slug}">Add to order</button>`;
}
function update() {
  try { localStorage.setItem("dsh-cart2", JSON.stringify(cart)); } catch (e) {}
  const s = subtotal(), f = feeFor(s), n = count(), left = CONFIG.FREE_OVER - s;
  $$("[data-cartcount]").forEach(e => e.textContent = n);
  $$("[data-qty]").forEach(e => e.innerHTML = qtyHTML(e.dataset.qty));
  $("#fab").textContent = `View order · ${inr(s)}`;
  $("#fab").classList.toggle("on", n > 0 && !$("#drawer").classList.contains("on"));
  $("#shipTxt").innerHTML = s === 0 ? `Free delivery over <b>${inr(CONFIG.FREE_OVER)}</b>. ${inr(CONFIG.FEE)} below. We deliver anywhere.`
    : left > 0 ? `Add <b>${inr(left)}</b> more for <b>free delivery</b>` : `✨ You have unlocked <b>free delivery</b>`;
  $("#shipBar").style.width = Math.min(100, s / CONFIG.FREE_OVER * 100) + "%";
  $("#lines").innerHTML = n ? Object.entries(cart).map(([k, q]) => { const d = dishes[k]; return `<div class="line"><img src="${BASE}${d.img}" alt=""><div>${d.name}<small>${inr(d.price)} each</small>${qtyHTML(k)}</div><b>${inr(d.price * q)}</b></div>`; }).join("") : `<p class="empty">Your order is empty. Explore the menu and add something delicious.</p>`;
  $("#sum").innerHTML = n ? `<div><span>Subtotal</span><span>${inr(s)}</span></div><div><span>Delivery</span><span>${f ? inr(f) : "Free"}</span></div><div class="t"><span>Total</span><span>${inr(s + f)}</span></div>` : "";
  $("#upiBtn").href = `upi://pay?pa=${CONFIG.UPI_ID}&pn=${encodeURIComponent(CONFIG.PAYEE)}&am=${s + f}&cu=INR&tn=${encodeURIComponent("Dragon Steak House order")}`;
  $("#upiBtn").style.display = n && $("#co").pay.value === "upi" ? "" : "none";
}
document.addEventListener("click", e => {
  const b = e.target.closest("[data-a]"); if (!b) return;
  const k = b.dataset.s, d = b.dataset.a === "+" ? 1 : -1;
  cart[k] = (cart[k] || 0) + d; if (cart[k] <= 0) delete cart[k];
  update();
});
const open = on => { $("#drawer").classList.toggle("on", on); $("#scrim").classList.toggle("on", on); update(); };
document.addEventListener("click", e => { if (e.target.closest("[data-opencart]") || e.target.closest("#fab")) open(true); });
$("#closeCart").onclick = $("#scrim").onclick = () => open(false);
$("#co").onchange = update;

$("#loc").onclick = () => navigator.geolocation ? navigator.geolocation.getCurrentPosition(p => {
  loc = `https://maps.google.com/?q=${p.coords.latitude},${p.coords.longitude}`; $("#loc").textContent = "📍 Location added ✓";
}, () => alert("Could not get your location. Please type the address.")) : alert("Location is not supported on this device.");

function message(f) {
  const s = subtotal(), fe = feeFor(s), m = ["*New order: Dragon Steak House*", ""];
  Object.entries(cart).forEach(([k, q]) => m.push(`${q} x ${dishes[k].name} = ${inr(dishes[k].price * q)}`));
  m.push("", `Subtotal: ${inr(s)}`, `Delivery: ${fe ? inr(fe) : "Free"} (final fee confirmed by distance)`, `*Total: ${inr(s + fe)}*`, "",
    `Name: ${f.name.value}`, `Phone: ${f.phone.value}`, `Address: ${f.addr.value}`);
  if (loc) m.push(`Location: ${loc}`);
  const upi = f.pay.value === "upi";
  m.push(`Payment: ${upi ? "UPI / Google Pay" : "Cash on delivery"}`);
  if (upi) m.push(`UPI: upi://pay?pa=${CONFIG.UPI_ID}&pn=${encodeURIComponent(CONFIG.PAYEE)}&am=${s + fe}&cu=INR`);
  return m.join("\n");
}
$("#co").onsubmit = e => {
  e.preventDefault();
  if (!count()) return alert("Please add a dish to your order first.");
  const t = encodeURIComponent(message(e.target));
  window.open(e.submitter.dataset.ch === "tg" ? `https://t.me/+${CONFIG.PHONE}?text=${t}` : `https://wa.me/${CONFIG.PHONE}?text=${t}`, "_blank");
};

// menu filter tabs
$$(".tabs button").forEach(b => b.onclick = () => {
  $$(".tabs button").forEach(x => x.classList.toggle("on", x === b));
  const c = b.dataset.cat; $$(".cat").forEach(s => s.style.display = c === "all" || s.dataset.cat === c ? "" : "none");
});
// header, mobile nav, reveal
const hdr = $(".hdr"), nav = $(".nav");
addEventListener("scroll", () => hdr.classList.toggle("solid", scrollY > 30), { passive: true }); hdr.classList.toggle("solid", scrollY > 30);
$(".burger").onclick = () => nav.classList.toggle("on");
$$(".nav a").forEach(a => a.onclick = () => nav.classList.remove("on"));
const io = new IntersectionObserver(es => es.forEach(x => x.isIntersecting && (x.target.classList.add("in"), io.unobserve(x.target))), { threshold: .1 });
$$(".reveal").forEach(el => io.observe(el));
update();
