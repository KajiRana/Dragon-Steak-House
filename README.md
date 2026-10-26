# Dragon Steak House

Multi-page website and direct-ordering site for **Dragon Steak House – Bar & Restaurant**, Temb Vaddo beach, Morjim, Goa 403512. Rated 4.4 on Google, open daily 7 am–11 pm.

Live: https://dragon-steak-house.vercel.app (auto-deploys from `main` on Vercel)
[Google Maps listing](https://www.google.co.in/maps/place/Dragon+Steak+House/@15.6182533,73.7348903,17z/data=!3m1!4b1!4m6!3m5!1s0x3bbfe9f9f8fcde5b:0x385e6ba110c0665b!8m2!3d15.6182481!4d73.7374652!16s%2Fg%2F11h8jy7752)

## Pages
| Page | Purpose |
|---|---|
| `index.html` | Home: hero, signature dishes, story, how delivery works |
| `menu.html` | Full menu with category filter and add-to-order |
| `dishes/<slug>.html` | One page per dish: photo, description, ingredients, allergens, spice, pairing, related dishes (12 pages) |
| `about.html` | Our story |
| `visit.html` | Address, hours, embedded map, contact, delivery FAQ |

Design: light ivory, terracotta and sage palette, Cormorant Garamond serif, arched photography, scroll reveals, floating dish photos, hover zoom, mobile-first.

## Ordering and delivery
- Cart drawer on every page, saved in the browser.
- **No distance limit.** Free delivery at a food subtotal of ₹1000 or more, ₹50 below that in the local zone. For farther addresses the fee is confirmed by distance over chat before payment.
- Checkout opens a pre-filled order in **WhatsApp** or **Telegram** (+91 86985 64244). Pay by **UPI / Google Pay** (`kajirana94@oksbi`, with a one-tap pay button) or cash on delivery.
- Settings live in `CONFIG` at the top of `cart.js`.

## Editing the menu
The menu is generated. Edit `data/dishes.json`, then run:

```
python3 build.py
```

This rewrites every page, `menu.js`, `sitemap.xml` and `robots.txt`. Commit and push to redeploy. Set `SITE` in `build.py` once a custom domain is added.

## Before relying on it (owner)
1. **Prices are estimates.** No public source lists this restaurant's itemised menu or prices (Zomato and Restaurant Guru block automated access and show no item list). Dishes are based on the chalkboard in the Google Maps photo and dishes guests mention in reviews (momos, seafood, steaks, noodles and rice). Confirm names and prices in `data/dishes.json`.
2. **Photos are illustrative.** Dish photos are free-licence Unsplash images, not photos of the restaurant's own plates. Replace them by dropping files into `assets/dishes/` with the same names. The storefront photo (`assets/hero.jpg`) is from the Google Maps listing.
3. Add the phone number and this website to the Google Business Profile.
4. Optional: Restaurant Guru lists a WhatsApp number (99753 04260) in an owner reply. This site uses +91 86985 64244.

## Hosting
Static site, no build step needed to serve. Vercel project `dragon-steak-house`, connected to this repository.
