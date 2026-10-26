// Site config. Owner: set UPI_ID to receive in-app UPI / Google Pay payments.
const CONFIG = {
  PHONE: "918698564244",
  UPI_ID: "",            // e.g. "yourname@okhdfcbank" — leave empty to confirm payment over chat
  PAYEE: "Dragon Steak House",
  FREE_OVER: 1000,       // food subtotal at or above this ships free
  FEE: 50,               // delivery fee below the threshold
  OPEN: 7, CLOSE: 23     // IST hours
};
const $ = s => document.querySelector(s), inr = n => "₹" + n.toLocaleString("en-IN");
const items = Object.fromEntries(MENU.flatMap(c => c.items.map(i => [i.id, i])));
let cart = {}, loc = null;
try { cart = JSON.parse(localStorage.getItem("dsh-cart") || "{}"); } catch (e) {}
for (const k in cart) if (!items[k]) delete cart[k];

const subtotal = () => Object.entries(cart).reduce((s, [id, q]) => s + items[id].price * q, 0);
const count = () => Object.values(cart).reduce((a, b) => a + b, 0);
const fee = s => (s === 0 || s >= CONFIG.FREE_OVER ? 0 : CONFIG.FEE);

function renderMenu() {
  $("#tabs").innerHTML = MENU.map((c, i) => `<button class="${i ? "" : "on"}" data-c="${i}">${c.cat}</button>`).join("");
  $("#menuList").innerHTML = MENU.map((c, i) => `<div class="cat reveal" id="cat${i}"><h3>${c.cat}</h3><div class="grid">${c.items.map(d => `
    <div class="dish"><h4><span>${d.veg ? '<i class="vg"></i>' : ""}${d.name}${d.tag ? `<span class="badge">${d.tag}</span>` : ""}</span><em>${inr(d.price)}</em></h4>
    <p>${d.desc}</p><div class="qty" data-id="${d.id}"></div></div>`).join("")}</div></div>`).join("");
  $("#tabs").onclick = e => { const b = e.target.closest("button"); if (!b) return;
    document.querySelectorAll("#tabs button").forEach(x => x.classList.toggle("on", x === b));
    $("#cat" + b.dataset.c).scrollIntoView({ behavior: "smooth", block: "start" }); };
  observe();
}
function renderQty() {
  document.querySelectorAll(".qty").forEach(el => {
    const q = cart[el.dataset.id] || 0;
    el.innerHTML = q ? `<div class="stepper"><button data-a="-">−</button>${q}<button data-a="+">+</button></div>` : `<button class="add" data-a="+">Add</button>`;
  });
}
function change(id, d) { cart[id] = (cart[id] || 0) + d; if (cart[id] <= 0) delete cart[id]; update(); }
document.addEventListener("click", e => {
  const q = e.target.closest("[data-a]"); if (!q) return;
  const id = q.closest("[data-id]").dataset.id; change(id, q.dataset.a === "+" ? 1 : -1);
});

function update() {
  try { localStorage.setItem("dsh-cart", JSON.stringify(cart)); } catch (e) {}
  const s = subtotal(), f = fee(s), n = count();
  $("#cartCount").textContent = n; $("#fabTot").textContent = inr(s);
  $("#fab").classList.toggle("on", n > 0 && !$("#drawer").classList.contains("on"));
  renderQty();
  const left = CONFIG.FREE_OVER - s;
  $("#shipTxt").innerHTML = s === 0 ? `Free delivery above ${inr(CONFIG.FREE_OVER)}. ${inr(CONFIG.FEE)} below.`
    : left > 0 ? `Add <b>${inr(left)}</b> more for <b>free delivery</b>` : `🎉 You unlocked <b>free delivery</b>`;
  $("#shipBar").style.width = Math.min(100, s / CONFIG.FREE_OVER * 100) + "%";
  $("#lines").innerHTML = n ? Object.entries(cart).map(([id, q]) => `<div class="line"><div>${items[id].name}<small>${inr(items[id].price)} each</small></div>
    <div class="qty" data-id="${id}"><div class="stepper"><button data-a="-">−</button>${q}<button data-a="+">+</button></div></div><b>${inr(items[id].price * q)}</b></div>`).join("") : `<p class="empty">Your cart is empty. Pick something delicious.</p>`;
  $("#sum").innerHTML = n ? `<div><span>Subtotal</span><span>${inr(s)}</span></div><div><span>Delivery</span><span>${f ? inr(f) : "FREE"}</span></div><div class="t"><span>Total</span><span>${inr(s + f)}</span></div>` : "";
}
const drawer = open => { $("#drawer").classList.toggle("on", open); $("#scrim").classList.toggle("on", open); update(); };
["#openCart", "#fab"].forEach(s => $(s).onclick = () => drawer(true));
["#closeCart", "#scrim"].forEach(s => $(s).onclick = () => drawer(false));

$("#loc").onclick = () => navigator.geolocation ? navigator.geolocation.getCurrentPosition(p => {
  loc = `https://maps.google.com/?q=${p.coords.latitude},${p.coords.longitude}`; $("#loc").textContent = "📍 Location added ✓";
}, () => alert("Couldn't get location. Please type your address.")) : alert("Location not supported.");

function message(f) {
  const s = subtotal(), fe = fee(s), m = [`*New order: Dragon Steak House*`, ""];
  Object.entries(cart).forEach(([id, q]) => m.push(`${q} x ${items[id].name} = ${inr(items[id].price * q)}`));
  m.push("", `Subtotal: ${inr(s)}`, `Delivery: ${fe ? inr(fe) : "FREE"}`, `*Total: ${inr(s + fe)}*`, "",
    `Name: ${f.name.value}`, `Phone: ${f.phone.value}`, `Address: ${f.addr.value}`);
  if (loc) m.push(`Location: ${loc}`);
  const upi = f.pay.value === "upi";
  m.push(`Payment: ${upi ? "UPI / Google Pay" : "Cash on delivery"}`);
  if (upi && CONFIG.UPI_ID) m.push(`Pay link: upi://pay?pa=${CONFIG.UPI_ID}&pn=${encodeURIComponent(CONFIG.PAYEE)}&am=${s + fe}&cu=INR`);
  return m.join("\n");
}
$("#co").onsubmit = e => {
  e.preventDefault();
  if (!count()) return alert("Add something to your cart first.");
  const t = encodeURIComponent(message(e.target)), ch = e.submitter.dataset.ch;
  window.open(ch === "tg" ? `https://t.me/+${CONFIG.PHONE}?text=${t}` : `https://wa.me/${CONFIG.PHONE}?text=${t}`, "_blank");
};

function openStatus() {
  const h = +new Date().toLocaleString("en-US", { timeZone: "Asia/Kolkata", hour: "numeric", hour12: false }) % 24;
  const o = h >= CONFIG.OPEN && h < CONFIG.CLOSE, el = $("#openNow");
  el.className = "open" + (o ? "" : " closed");
  el.innerHTML = `<i></i>${o ? "Open now · until 11 pm" : "Closed now · opens at 7 am. Pre-order anytime"}`;
}
function observe() {
  const io = new IntersectionObserver(es => es.forEach(x => x.isIntersecting && (x.target.classList.add("in"), io.unobserve(x.target))), { threshold: .12 });
  document.querySelectorAll(".reveal:not(.in)").forEach(el => io.observe(el));
}
addEventListener("scroll", () => $("#nav").classList.toggle("solid", scrollY > 40), { passive: true });
$("#yr").textContent = new Date().getFullYear();
renderMenu(); openStatus(); update(); observe();
