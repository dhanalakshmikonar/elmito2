from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from apps.orders import views as order_views
from store import views
urlpatterns = [
 path('admin/', admin.site.urls), path('', views.home, name='home'), path('shop/', views.shop, name='shop'),
 path('men/', views.category_page, {'audience':'men'}, name='men'), path('women/', views.category_page, {'audience':'women'}, name='women'), path('kids/', views.category_page, {'audience':'kids'}, name='kids'),
 path('product/<slug:slug>/', views.product_detail, name='product'), path('bag/', views.cart, name='cart'), path('bag/add/<slug:slug>/', views.add_to_cart, name='add_to_cart'), path('bag/update/<int:item_id>/', views.update_cart, name='update_cart'), path('bag/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
 path('checkout/', order_views.checkout, name='checkout'), path('orders/', order_views.order_list, name='orders'), path('login/', views.login_page, name='login'), path('verify/', views.verify_page, name='verify'), path('about/', views.about, name='about'), path('contact/', views.contact, name='contact'),
 path('privacy-policy/', views.legal, {'page':'privacy'}, name='privacy'), path('terms-and-conditions/', views.legal, {'page':'terms'}, name='terms'), path('returns-and-refunds/', views.legal, {'page':'returns'}, name='returns'),
 path('account/', include('apps.accounts.urls')), path('cart/', include('apps.cart.urls')), path('', include('apps.orders.urls')), path('', include('apps.payments.urls')), path('', include('apps.products.urls')), path('', include('apps.core.urls')),
]
if settings.DEBUG or settings.SERVE_MEDIA: urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

