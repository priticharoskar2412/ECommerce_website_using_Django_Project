from django.urls import path
from .views import CartView, AddToCartView, UpdateCartItemView, RemoveCartItemView, CheckoutView

app_name = 'cart'

urlpatterns = [
    path('', CartView.as_view(), name='cart_view'),
    path('add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('update/<int:item_id>/', UpdateCartItemView.as_view(), name='update_cart'),
    path('remove/<int:item_id>/', RemoveCartItemView.as_view(), name='remove_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
