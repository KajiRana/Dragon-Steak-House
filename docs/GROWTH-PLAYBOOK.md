# Dragon Steak House: growth playbook

Website features are live. These are the owner-side actions that drive orders. Work top to bottom.

## Week 1: foundations
- [ ] **Confirm the menu and prices** in `data/dishes.json` (current prices are estimates), then `python3 build.py` and push.
- [ ] **Photograph 20 to 30 real dishes** in daylight near the upstairs window. Replace the files in `assets/dishes/` keeping the same names. Real photos replace the stock ones.
- [ ] **Google Business Profile** (business.google.com):
  - Add phone +91 86985 64244 and website https://dragon-steak-house.vercel.app
  - Set "Order online" and "Menu" links to `/menu.html`, "Reservations" to `/events.html`
  - Upload the real photos, set categories: Restaurant, Steak house, Seafood restaurant, Breakfast restaurant
  - Post weekly (a dish, an offer, a sunset). Reply to every review within 24 hours
- [ ] Ask every happy table and delivery customer for a Google review (add the review link to the WhatsApp confirmation).
- [ ] Enable **Vercel Web Analytics** in the Vercel dashboard (Project → Analytics → Enable). The site already loads the script and sends events: `add_to_cart`, `open_cart`, `send_order`, `enquiry`.

## Week 2: partners and repeat orders
- [ ] Open `/partners.html`, create a QR card for each nearby villa, hostel and guesthouse, print and drop them off. Orders arrive tagged "Referred by: <property>". Offer partners a monthly thank-you, such as a free feast for every 10 referred orders.
- [ ] Put a QR card (or sticker) in every delivery bag, pointing to the site.
- [ ] Save every customer number in a **WhatsApp Business broadcast list**. Send at most two messages a week: breakfast at 8 am, sunset feast at 5 pm.
- [ ] Honour the **loyalty treat**: the order message says "Loyalty: order #6, free Fresh Lime Soda". The website counts orders per device. Check the customer's chat history when in doubt.

## Instagram plan (3 posts a week, Reels first)
| Day | Content |
|---|---|
| Mon | Reel: steak on the open flame, 7 to 10 seconds, sizzling sound |
| Wed | Carousel: a feast laid out on the upstairs table with the river behind |
| Fri | Reel: momos being pleated and steamed, ending on the dip |
| Stories daily | Today's chalkboard, sunset from upstairs, a happy delivery |

Bio link: the website. Use location tag "Morjim Beach" and tags such as #morjim #ashwem #northgoa #goafood #goadelivery. Russian captions on alternate posts.

## Zomato and Swiggy
Use them for discovery only. Every aggregator order bag gets the QR card: "Order direct next time, ₹50 off your first direct order."

## Monthly review
Check in Vercel Analytics: visits, add-to-cart and send-order counts, top dishes. Promote what sells, cut what doesn't, and update combos.
