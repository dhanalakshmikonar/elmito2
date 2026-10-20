from decimal import Decimal
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

PRODUCTS = [
    {"name":"Essential Oversized Tee","slug":"essential-oversized-tee","price":1499,"category":"Oversized","color":"Olive","badge":"New arrival","tone":"olive","image":"https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=1000&q=85","desc":"A considered everyday uniform. Relaxed proportions, substantial cotton and a clean, confident silhouette."},
    {"name":"Relaxed Fit Tee","slug":"relaxed-fit-tee","price":1299,"category":"Essentials","color":"Stone","badge":"","tone":"stone","image":"https://images.unsplash.com/photo-1527719327859-c6ce80353573?auto=format&fit=crop&w=1000&q=85","desc":"An easy, versatile fit with a soft hand-feel and understated finish."},
    {"name":"Graphic Tee","slug":"graphic-tee","price":1299,"category":"Graphic","color":"White","badge":"Bestseller","tone":"white","image":"https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?auto=format&fit=crop&w=1000&q=85","desc":"Quietly expressive graphics on a premium cotton base."},
    {"name":"Core Tee","slug":"core-tee","price":1199,"category":"Essentials","color":"Black","badge":"","tone":"black","image":"https://images.unsplash.com/photo-1523381210434-271e8be1f52b?auto=format&fit=crop&w=1000&q=85","desc":"The foundational tee. Clean lines, thoughtful construction, everyday comfort."},
    {"name":"Minimal Tee","slug":"minimal-tee","price":1299,"category":"Essentials","color":"Black","badge":"","tone":"black","image":"https://images.unsplash.com/photo-1503341504253-dff4815485f1?auto=format&fit=crop&w=1000&q=85","desc":"Minimal by design, made to be worn on repeat."},
    {"name":"Urban Tee","slug":"urban-tee","price":1399,"category":"Oversized","color":"Moss","badge":"Limited","tone":"olive","image":"https://images.unsplash.com/photo-1576566588028-4147f3842f27?auto=format&fit=crop&w=1000&q=85","desc":"A bolder, boxy shape in a grounded, versatile palette."},
    {"name":"Classic Tee","slug":"classic-tee","price":1199,"category":"Essentials","color":"Black","badge":"","tone":"black","image":"https://images.unsplash.com/photo-1562157873-818bc0726f68?auto=format&fit=crop&w=1000&q=85","desc":"A timeless fit that lets the fabric and cut speak for themselves."},
    {"name":"Co-ord Tee","slug":"coord-tee","price":1499,"category":"Co-ord","color":"Ecru","badge":"New","tone":"stone","image":"https://images.unsplash.com/photo-1618354691373-d851c5c3a990?auto=format&fit=crop&w=1000&q=85","desc":"Designed to pair effortlessly with the rest of your wardrobe."},
]

def money(value):
    return "₹{:,.0f}".format(value)

def with_prices(products):
    return [{**p, "price_display": money(p["price"])} for p in products]

def home(request):
    return render(request, "store/home.html", {"featured": with_prices(PRODUCTS[:4]), "new_arrivals": with_prices(PRODUCTS[4:8])})

def shop(request):
    products = PRODUCTS
    category = request.GET.get("category", "").strip()
    query = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "featured")
    if category:
        products = [p for p in products if p["category"].lower() == category.lower()]
    if query:
        products = [p for p in products if query.lower() in (p["name"] + " " + p["category"] + " " + p["color"]).lower()]
    if sort == "price-low":
        products = sorted(products, key=lambda p: p["price"])
    elif sort == "price-high":
        products = sorted(products, key=lambda p: p["price"], reverse=True)
    return render(request, "store/shop.html", {"products": with_prices(products), "category": category, "query": query, "sort": sort})

def product_detail(request, slug):
    product = next((p for p in PRODUCTS if p["slug"] == slug), None)
    if not product:
        return redirect("shop")
    related = [p for p in PRODUCTS if p["slug"] != slug][:4]
    return render(request, "store/product.html", {"product": {**product, "price_display": money(product["price"])}, "related": with_prices(related)})

@require_POST
def add_to_cart(request, slug):
    product = next((p for p in PRODUCTS if p["slug"] == slug), None)
    if not product:
        return redirect("shop")
    cart = request.session.get("cart", {})
    size = request.POST.get("size", "M")
    key = f"{slug}:{size}"
    item = cart.get(key, {"slug": slug, "size": size, "quantity": 0})
    item["quantity"] = min(int(item.get("quantity", 0)) + max(1, int(request.POST.get("quantity", 1))), 10)
    cart[key] = item
    request.session["cart"] = cart
    messages.success(request, "Added to your bag.")
    return redirect("cart")

def _cart_items(request):
    cart = request.session.get("cart", {})
    items, subtotal = [], 0
    for key, item in cart.items():
        product = next((p for p in PRODUCTS if p["slug"] == item.get("slug")), None)
        if product:
            quantity = int(item.get("quantity", 1))
            line = product["price"] * quantity
            items.append({**product, "key": key, "size": item.get("size", "M"), "quantity": quantity, "line_total": money(line), "price_display": money(product["price"])})
            subtotal += line
    shipping = 0 if subtotal >= 2999 or subtotal == 0 else 99
    return items, subtotal, shipping

def cart(request):
    items, subtotal, shipping = _cart_items(request)
    return render(request, "store/cart.html", {"items": items, "subtotal": money(subtotal), "shipping": money(shipping), "total": money(subtotal + shipping), "subtotal_raw": subtotal})

@require_POST
def update_cart(request, slug):
    cart = request.session.get("cart", {})
    key = request.POST.get("key", "")
    if key in cart and cart[key].get("slug") == slug:
        try:
            qty = int(request.POST.get("quantity", 1))
            if qty <= 0:
                cart.pop(key, None)
            else:
                cart[key]["quantity"] = min(qty, 10)
        except ValueError:
            pass
    request.session["cart"] = cart
    return redirect("cart")

@require_POST
def remove_from_cart(request, slug):
    cart = request.session.get("cart", {})
    key = request.POST.get("key", "")
    if key in cart and cart[key].get("slug") == slug:
        cart.pop(key, None)
    request.session["cart"] = cart
    return redirect("cart")

def checkout(request):
    items, subtotal, shipping = _cart_items(request)
    if request.method == "POST":
        messages.info(request, "This starter checkout is a design demo. Connect your order and Razorpay services before accepting real payments.")
    return render(request, "store/checkout.html", {"items": items, "subtotal": money(subtotal), "shipping": money(shipping), "total": money(subtotal + shipping)})

def login_page(request):
    return render(request, "store/login.html")

def verify_page(request):
    return render(request, "store/verify.html")

def orders_page(request):
    return render(request, "store/orders.html")

def about(request):
    return render(request, "store/about.html")

def contact(request):
    return render(request, "store/contact.html")
