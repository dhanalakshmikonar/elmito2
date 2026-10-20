# EL MITO — Django Design Starter

A responsive Django storefront inspired by the approved EL MITO design direction: warm ivory, charcoal, muted olive, generous whitespace, editorial product imagery and restrained interactions.

## Run locally
1. Install Python 3.10+.
2. Create/activate a virtual environment.
3. `pip install -r requirements.txt`
4. `python manage.py migrate`
5. `python manage.py runserver`
6. Open http://127.0.0.1:8000/

## Pages
Home, Shop, Product details, Cart, Checkout, Login, OTP verification, My Orders, About and Contact.

## Important
This ZIP implements the Django-powered design starter and a demo session cart. Product catalogue content is sample data and images load from Unsplash URLs. Checkout is a UI demo only: no real order creation, OTP delivery, email, WhatsApp or Razorpay transaction is enabled. Before production, connect your existing EL MITO models/services and implement server-side payment verification, inventory reservation, rate limits, validation and production settings. Never add secrets to source control.
