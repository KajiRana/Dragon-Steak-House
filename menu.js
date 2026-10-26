// Menu data. Dishes come from the "Today's Menu" blackboard in the Google Maps photo.
// PRICES ARE ESTIMATES (₹) — owner must confirm before launch. Edit here only; the site rebuilds from this list.
window.MENU = [
  { cat: "Seafood Specials", items: [
    { id: "kf-thali", name: "King Fish Thali", desc: "Goan fish curry, fried kingfish, rice, sol kadi, sides", price: 450, tag: "popular" },
    { id: "kf-fillet", name: "King Fish Fillet", desc: "Pan-seared fillet with garlic butter and greens", price: 520 },
    { id: "sea-stir", name: "Seafood Stir Fry", desc: "Prawns, calamari and fish tossed in chilli-garlic wok sauce", price: 480 },
    { id: "sea-pasta", name: "Seafood Pasta", desc: "Creamy or tomato sauce with mixed Goan seafood", price: 420 }
  ]},
  { cat: "Steaks & Grill", items: [
    { id: "steak-bp", name: "Steaks Burger Platter", desc: "Juicy steak burger, fries, grilled veg and house sauce", price: 480, tag: "popular" },
    { id: "chk-steak", name: "Chicken Steak", desc: "Herb-marinated chicken steak with mash and pepper sauce", price: 380 },
    { id: "chk-tikka", name: "Chicken Tikka Platter", desc: "Charred tikka with mint chutney and onion rings", price: 360 }
  ]},
  { cat: "Thai & Asian", items: [
    { id: "thai-non", name: "Thai Curry (Non-Veg)", desc: "Coconut Thai curry with jasmine rice", price: 380 },
    { id: "thai-veg", name: "Veg Thai Curry", desc: "Seasonal vegetables in green or red coconut curry", price: 320, veg: true },
    { id: "momo", name: "Spinach Momos", desc: "Steamed spinach and cheese momos with spicy dip", price: 220, veg: true, tag: "popular" },
    { id: "noodles", name: "Hakka Noodles", desc: "Wok-tossed noodles, choose veg, egg or chicken", price: 240 },
    { id: "rice", name: "Fried Rice", desc: "Wok fried rice, choose veg, egg or chicken", price: 230 }
  ]},
  { cat: "Drinks", items: [
    { id: "lime", name: "Fresh Lime Soda", desc: "Sweet, salted or mixed", price: 90, veg: true },
    { id: "coconut", name: "Tender Coconut", desc: "Straight from the Morjim palms", price: 80, veg: true }
  ]}
];
