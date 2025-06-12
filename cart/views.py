from django.views import View
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from .models import Cart, CartItem, Order, OrderItem
from core.models import Product


class CartDetailView(LoginRequiredMixin, DetailView):
    model = Cart
    template_name = 'cart/cart_detail.html'
    context_object_name = 'cart'

    def get_object(self, queryset=None):
        cart, _ = Cart.objects.get_or_create(user=self.request.user, is_active=True)
        return cart


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs['product_id'])
        cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            if cart_item.quantity < product.quantity:
                cart_item.quantity += 1
                cart_item.save()
                messages.success(request, f'"{product.name}" quantity increased in your cart.')
            else:
                messages.error(request, f'Cannot add more "{product.name}" than available in stock ({product.quantity}).')
        else:
            if product.quantity > 0:
                cart_item.quantity = 1
                cart_item.save()
                messages.success(request, f'"{product.name}" added to your cart.')
            else:
                cart_item.delete()
                messages.error(request, f'"{product.name}" is currently out of stock.')

        return redirect(request.META.get('HTTP_REFERER', 'core:index'))


class UpdateCartItemView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user, is_active=True)
        item = get_object_or_404(CartItem, cart=cart, id=kwargs['item_id'])

        action = request.POST.get('action')
        if action == 'increment':
            if item.quantity < item.product.quantity:
                item.quantity += 1
                item.save()
                messages.success(request, 'Product quantity increased.')
            else:
                messages.error(request, f'Maximum quantity reached ({item.product.quantity}).')
        elif action == 'decrement':
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
                messages.success(request, 'Product quantity decreased.')
            else:
                item.delete()
                messages.success(request, 'Product removed from your cart.')

        return redirect('cart:cart_detail')


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user, is_active=True)
        item = get_object_or_404(CartItem, cart=cart, id=kwargs['item_id'])
        item.delete()
        messages.success(request, 'Product removed from your cart.')
        return redirect('cart:cart_detail')


class CreateOrderView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            cart = Cart.objects.select_for_update().filter(user=request.user, is_active=True).first()
            if not cart or not cart.items.exists():
                messages.error(request, 'Your cart is empty or does not exist.')
                return redirect('cart:cart_detail')

            order = Order.objects.create(user=request.user, cart=cart, status='pending')

            for item in cart.items.select_related('product').all():
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

                product = item.product
                if product.quantity >= item.quantity:
                    product.quantity -= item.quantity
                    product.save()
                else:
                    messages.error(request, f'Not enough stock for product "{product.name}".')
                    transaction.set_rollback(True)
                    return redirect('cart:cart_detail')

            cart.is_active = False
            cart.save()

        messages.success(request, f'Order #{order.id} has been placed successfully.')
        return redirect('cart:order_list')


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'cart/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        items = order.items.all()

        for item in items:
            item.total_price = item.quantity * item.product.price
        
        total = sum(item.total_price for item in items)
        context['order'] = order
        context['items'] = items
        context['order_total'] = total
        return context
    
class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'cart/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
