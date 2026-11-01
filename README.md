# Dragon Steak House

Multi-page website and direct-ordering site for **Dragon Steak House – Bar & Restaurant**, Temb Vaddo beach, Morjim, Goa 403512. Rated 4.4 on Google, open daily 7 am–11 pm.

- Live: https://dragon-steak-house.vercel.app (auto-deploys from `main` on Vercel)
- [Google Maps listing](https://www.google.co.in/maps/place/Dragon+Steak+House/@15.6182533,73.7348903,17z/data=!3m1!4b1!4m6!3m5!1s0x3bbfe9f9f8fcde5b:0x385e6ba110c0665b!8m2!3d15.6182481!4d73.7374652!16s%2Fg%2F11h8jy7752)
- Owner action plan: [`docs/GROWTH-PLAYBOOK.md`](docs/GROWTH-PLAYBOOK.md)

## Pages
| Page | Purpose |
|---|---|
| `index.html` | Home: animated hero, morning breakfast block (before 11 am), feasts, signature dishes, story, how delivery works |
| `menu.html` | Full menu with category filter (`menu.html#Combos` opens one category) |
| `dishes/<slug>.html` | One page per dish (20): photo, description, Russian name, ingredients, allergens, spice, serving, "travels well" note, pairing, related dishes |
| `offers.html` | Welcome offer, free delivery, loyalty, feasts, breakfast, celebrations |
| `gallery.html` | Photo gallery with lightbox |
| `events.html` | Birthdays and group dinners, enquiry form that opens WhatsApp |
| `about.html` | Our story |
| `visit.html` | Address, hours, map, contact, delivery FAQ, table booking form |
| `menu-ru.html` | Russian menu (Меню на русском) with ordering |
| `partners.html` | Printable QR menu cards for villas and guesthouses (not indexed) |

## Ordering, delivery and sales features
- Cart drawer on every page, saved in the browser. Add-to-order shows a toast and flies a dot to the cart.
- **Delivery:** no distance limit. Free at a food subtotal of ₹1000 or more, ₹50 below that in the local zone (`LOCAL_KM`, default 5 km). When the customer shares a location the cart shows the distance. Beyond the local zone the fee is confirmed on chat before payment.
- **Upsell:** the cart suggests dishes that close the gap to free delivery, or a drink or dessert.
- **Welcome offer:** ₹50 off the first direct order of ₹500 or more, applied in the cart (per device).
- **Loyalty:** every 6th order from a device is flagged in the message with a free Fresh Lime Soda.
- **Feasts:** Couple's Feast ₹999, Family Seafood Feast ₹1,599, Veggie Feast ₹899, each cheaper than a la carte.
- **Scheduling:** "As soon as possible" or "Schedule for later". When closed, scheduling is preselected.
- **Checkout:** pre-filled order in **WhatsApp** or **Telegram** (+91 86985 64244). Pay by **UPI / Google Pay** (`kajirana94@oksbi`, one-tap button) or cash on delivery.
- **Partner referrals:** QR cards link to `/?ref=<property>`. Orders include "Referred by".
- **Analytics:** Vercel Web Analytics script plus events `add_to_cart`, `open_cart`, `send_order`, `enquiry`. Enable Analytics in the Vercel project settings.
- **SEO:** Restaurant and MenuItem schema, sitemap, robots, Open Graph tags.

Settings live in `CONFIG` at the top of `cart.js`. Offer wording lives in `OFFERS` in `build.py`.

## Design
Light ivory, terracotta and sage palette. Cormorant Garamond with Inter. Custom dragon-and-flame logo (`assets/logo.svg`), line illustrations (palm, wave ornaments), arched photography, word-by-word headline reveal, rising smoke over the steak, swaying palm, scroll reveals, count-up stats, hover zoom, page transitions, and a mobile menu. Respects reduced-motion settings.

## Editing the menu
The site is generated. Edit `data/dishes.json`, then run:

```
python3 build.py
```

This rewrites every page, `menu.js`, `sitemap.xml`, `robots.txt` and `assets/logo.svg`. Commit and push to redeploy. Set `SITE` in `build.py` once a custom domain is added.

Dish fields: `price`, `cat`, `tag`, `veg`, `spice` (0–3), `travels` (holds up for delivery), `img` (reuse another dish's photo), `ru` (Russian name).

## Still needed from the owner
1. **Prices are estimates.** No public source lists this restaurant's itemised menu. Dishes come from the Google Maps chalkboard photo and from reviews, plus new breakfast, feast and dessert items. The King Fish item is shown as King Fish Rava Fry, since the restaurant does not serve a thali. Confirm everything in `data/dishes.json`.
2. **Photos.** The restaurant's own photos (shot on a realme 7 Pro, November 2026) are used for the venue and seafood. They were cropped to remove the camera watermark, colour-graded warm, sharpened and compressed to about 1600px. A guest in the dining-room shot is softly blurred.
   | File | Shows | Used on |
   |---|---|---|
   | `assets/gallery/deck.jpg` | Thatched upstairs deck | Home hero, gallery, Open Graph/schema image |
   | `assets/gallery/deck-trees.jpg` | Deck tables among the trees | Events, gallery |
   | `assets/gallery/about-dining.jpg` | Ground-floor dining room and bar, 4:5 crop (899×1124) of `dining-room.jpg` made to fit the arched frame | Our Story (About) hero |
   | `assets/gallery/bar.jpg` | Bar | Gallery |
   | `assets/gallery/dining-room.jpg` | Ground-floor dining and bar | Gallery |
   | `assets/gallery/storefront.jpg` | Front of the restaurant with the dome oven | Visit, gallery |
   | `assets/gallery/pizza-oven.jpg` | Wood-fired oven | Gallery |
   | `assets/gallery/fresh-catch.jpg` | Fish on ice | Gallery |
   | `assets/gallery/fresh-lobster.jpg` | Raw painted lobsters | Gallery |
   | `assets/gallery/staircase.jpg` | Stairs to the deck | Gallery |
   | `assets/dishes/lobster-thermidor.jpg` | Lobster plate as served | Family Seafood Feast card and page, gallery |

   Other dish photos are still illustrative free-licence images; replace files in `assets/dishes/` with real photos of the same names. The Unsplash scenery photos and the Google Maps storefront photo were removed.
   - `assets/dishes/king-fish-rava-fry.jpg` (King Fish Rava Fry): "Seer Fish Fry" by Nithin bolar k, Wikimedia Commons, CC BY-SA 3.0.
3. **WhatsApp number:** Restaurant Guru shows an owner reply pointing to 99753 04260. This site uses +91 86985 64244.
4. Google Business Profile, partner drop-offs and Instagram: see the playbook.

## Hosting
Static site, no build step needed to serve. Vercel project `dragon-steak-house`, connected to this repository.
