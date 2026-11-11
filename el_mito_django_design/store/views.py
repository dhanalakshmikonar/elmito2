from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from apps.cart.services import cart as cart_service
from apps.cart.services.cart import CartError
from apps.products.models import Category, CollectionItem, Product, ProductVariant
from apps.products.services import catalog


def money(value):
    return "₹{:,.2f}".format(value)

def _card(product):
    image = product.primary_image
    return {"name": product.name, "slug": product.slug, "price": product.selling_price,
            "price_display": money(product.selling_price), "category": product.category.name,
            "color": "", "badge": "New arrival" if product.is_new_arrival else "",
            "image": image.image.url if image and image.image else "", "desc": product.description,
            "record": product}

def home(request):
    products = catalog.visible_products()
    featured = list(products.filter(is_best_seller=True).order_by("-popularity")[:4])
    if not featured: featured = list(products.filter(is_featured=True)[:4])
    arrivals = list(products.filter(is_new_arrival=True)[:8])
    if not arrivals:
        arrivals = list(products.order_by("-created_at")[:8])
    collection_tiles = CollectionItem.objects.select_related("product").filter(
        is_active=True, product__status=Product.Status.ACTIVE
    ).order_by("position", "id")[:10]
    return render(request, "store/home.html", {"featured": [_card(p) for p in featured],
        "new_arrivals": [_card(p) for p in arrivals], "product_display": collection_tiles})
def category_page(request, audience):
    images = {"men": ["store/campaign/Gemini_Generated_Image_vwhd25vwhd25vwhd.png", "store/campaign/Gemini_Generated_Image_ny2xajny2xajny2x.png", "store/campaign/Gemini_Generated_Image_zi8zozi8zozi8zoz.png", "store/campaign/Gemini_Generated_Image_ctv1fkctv1fkctv1.png", "store/campaign/Minimalist Streetwear Editorial Couple.png"], "women": ["store/campaign/Gemini_Generated_Image_z1ujf2z1ujf2z1uj.png", "store/campaign/Minimalist Streetwear Editorial Couple.png", "store/campaign/Gemini_Generated_Image_ctv1fkctv1fkctv1.png", "store/campaign/Gemini_Generated_Image_z1ujf2z1ujf2z1uj.png", "store/campaign/Gemini_Generated_Image_ctv1fkctv1fkctv1.png"], "kids": ["store/campaign/kids-campaign.jpeg"] * 5}
    products = catalog.visible_products().filter(audience__in=[audience, "all"])
    return render(request, "store/category.html", {"category_name": audience.title(), "placeholders": [{"image": x} for x in images[audience]], "products": [_card(p) for p in products]})

def shop(request):
    filters = catalog.ProductFilters.from_querydict(request.GET)
    products = catalog.list_products(filters)
    category_slug = filters.category
    category_obj = Category.objects.filter(slug=category_slug, is_active=True).first() if category_slug else None
    return render(request, "store/shop.html", {"products": [_card(p) for p in products], "category": category_obj.name if category_obj else "", "category_slug": category_slug, "query": filters.q, "sort": filters.sort, "categories": Category.objects.filter(is_active=True), "facets": catalog.facets(), "filters": filters})
def product_detail(request, slug):
    product = get_object_or_404(catalog.visible_products(), slug=slug)
    matrix = catalog.variant_matrix(product)
    return render(request, "store/product.html", {"product": {**_card(product), "record": product}, "related": [_card(p) for p in catalog.related_products(product)], "matrix": matrix, "images": list(product.images.all()), "sizes": ProductVariant.Size.values})

def _line_image(line):
    product = line.product
    images = list(product.images.all())
    return next((i for i in images if i.color.lower() == line.variant.color.lower()), product.primary_image)

def cart(request):
    cart_obj = cart_service.get_cart(request)
    summary = cart_service.refresh(cart_obj, request.user)
    items = []
    for line in summary.lines:
        line.image_obj = _line_image(line)
        items.append({"product": line.product, "slug": line.product.slug, "name": line.product.name, "image": line.image_obj.image.url if line.image_obj else "", "color": line.variant.color, "size": line.variant.size, "quantity": line.quantity, "price_display": money(line.unit_price), "line_total": money(line.line_total), "item_id": line.item.pk})
    return render(request, "store/cart.html", {"items": items, "subtotal": money(summary.subtotal), "shipping": money(0), "total": money(summary.total), "subtotal_raw": summary.subtotal})

@require_POST
def add_to_cart(request, slug):
    product = get_object_or_404(catalog.visible_products(), slug=slug)
    try:
        variant = cart_service.resolve_variant(product_id=product.pk, variant_id=request.POST.get("variant"), color=request.POST.get("color", ""), size=request.POST.get("size", ""))
        cart_service.add_item(cart_service.get_cart(request, create=True), variant, request.POST.get("quantity", 1))
    except CartError as exc:
        messages.error(request, str(exc))
        return redirect("product", slug=slug)
    messages.success(request, "Added to your bag.")
    return redirect("cart")

@require_POST
def update_cart(request, item_id):
    try:
        cart_obj = cart_service.get_cart(request)
        if not cart_obj: raise CartError("Your bag is empty.")
        cart_service.set_quantity(cart_obj, item_id, request.POST.get("quantity"))
    except CartError as exc: messages.error(request, str(exc))
    return redirect("cart")

@require_POST
def remove_from_cart(request, item_id):
    try:
        cart_obj = cart_service.get_cart(request)
        if not cart_obj: raise CartError("Your bag is empty.")
        cart_service.remove_item(cart_obj, item_id)
    except CartError as exc: messages.error(request, str(exc))
    return redirect("cart")

def checkout(request):
    return redirect("orders:checkout")
def login_page(request): return redirect("accounts:login")
def verify_page(request): return redirect("accounts:verify_otp")
@login_required
def orders_page(request): return redirect("orders:list")
def about(request): return render(request, "store/about.html")
def contact(request):
    from apps.core.forms import ContactForm
    from apps.core.views import _rate_limited
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if _rate_limited(request, "contact"):
            form.add_error(None, "Please try again later.")
        else:
            form.save(); messages.success(request, "Thanks, your message has been received."); return redirect("contact")
    return render(request, "store/contact.html", {"form": form})

def legal(request, page): return render(request, f"pages/{page}.html")








