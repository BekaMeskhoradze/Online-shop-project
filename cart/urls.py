from django.urls import path
from .views import (
    CartDetailView,
    AddToCartView,
    UpdateCartItemView,
    RemoveFromCartView,
    CreateOrderView,
    OrderDetailView,
    OrderListView,
)

app_name = 'cart'

urlpatterns = [
    path('', CartDetailView.as_view(), name='cart_detail'),
    path('add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('item/update/<int:item_id>/', UpdateCartItemView.as_view(), name='update_cart_item'),
    path('item/remove/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('order/create/', CreateOrderView.as_view(), name='create_order'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
]