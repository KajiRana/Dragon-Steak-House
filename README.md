# Dragon Steak House

Website and direct-ordering site for **Dragon Steak House – Bar & Restaurant**, Temb Vaddo beach, Morjim, Goa 403512 (★ 4.4 on Google, open 7 am–11 pm daily).

## Features
- Dark, animated one-page site: Ken Burns hero, scroll reveals, sticky category tabs, live open/closed status.
- Menu with cart, saved in the browser between visits.
- **Delivery rule:** free at a food subtotal of ₹1000 or more, otherwise a flat ₹50. A progress bar nudges customers toward free delivery.
- Checkout sends a pre-filled order to **WhatsApp** or **Telegram** (+91 86985 64244). Payment by UPI / Google Pay or cash on delivery.
- Local SEO: Restaurant schema markup, meta description, mobile-first layout.

## Files
| File | Purpose |
|---|---|
| `index.html`, `style.css` | Page and design |
| `app.js` | Cart, delivery fee, checkout, open status. Settings are in `CONFIG` at the top |
| `menu.js` | Menu data. Edit dishes and prices here |
| `assets/hero.jpg` | Photo from the Google Maps listing |

## Before launch (owner)
1. **Confirm menu prices in `menu.js`.** Dishes come from the chalkboard in the Google Maps photo, but the **prices are estimates**.
2. Set `UPI_ID` in `app.js` so orders include a one-tap UPI payment link. Without it, payment is confirmed over chat.
3. Replace or add real food photos in `assets/`.
4. Add the phone number and website to the Google Business Profile.

## Run locally
Open `index.html` in a browser. No build step. To host it, deploy the folder to any static host, for example `wrangler pages deploy .` on Cloudflare Pages.
