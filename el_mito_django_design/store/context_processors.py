def cart_count(request):
    cart = request.session.get("cart", {})
    return {"cart_count": sum(int(v.get("quantity", 0)) for v in cart.values())}
