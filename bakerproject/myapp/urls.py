from django.urls import path
from myapp import views

urlpatterns = [
    path('register/',views.register_user,name='register'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),

    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('read_more_about/',views.read_more_about,name='read_more'),
    path('contact/',views.contact,name='contact'),

    path('product/',views.product,name="product"),
    path('products/category/<int:category_id>/',views.category_products,name='category_products'),
    path('product/<int:product_id>/',views.product_detail,name='product_detail'),

    path('service/',views.service,name="service"),
    path('team/',views.team,name='team'),
    path('testmonial/',views.testimonial,name='testimonial'),
    path('404/',views.error,name='404'),

    path('profile/',views.profile,name='profile'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),

    path('cart/add/<int:product_id>/',views.add_to_cart,name='add_to_cart'),
    path('cart/',views.cart,name='cart'),
    path('cart/update/<int:item_id>/<str:change>/',views.update_cart,name='update_cart'), 
    path('cart/remove/<int:item_id>/',views.remove_from_cart,name='remove_from_cart'),

    path('wishlist/',views.wishlist,name='wishlist'),
    path('wishlist/add/<int:product_id>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('wishlist/remove/<int:wishlist_id>/',views.remove_from_wishlist,name='remove_from_wishlist'),
    path("wishlist/move-to-cart/<int:wishlist_id>/", views.move_wishlist_to_cart, name="move_wishlist_to_cart"),

    path('checkout/',views.checkout,name='checkout'),
    path('order/success/<int:order_id>/',views.order_success,name='order_success'),
    path('my-orders/',views.my_orders,name='my_orders'),
    path('order/<int:order_id>/',views.order_detail,name='order_detail'),
    path('order/<int:order_id>/invoice/',views.download_invoice,name='download_invoice'),

    path("test-email/", views.test_email),

    
]
