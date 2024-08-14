from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [



    path('register/', RegisterView.as_view(), name='register'),

    path('', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('index/', IndexView.as_view(), name='index'),
    path('category/<slug:slug>/', IndexView.as_view(), name='category_foods'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('cart/', CartView.as_view(), name='cart'),
    path('addtocart/<int:food_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/update/<int:pk>/', CartItemUpdateView.as_view(), name='update_cart_item'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order/confirmation/<int:order_id>/', OrderConfirmationView.as_view(),name='order_confirmation'),
    path('order/history/', OrderHistoryView.as_view(), name='order_history'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
