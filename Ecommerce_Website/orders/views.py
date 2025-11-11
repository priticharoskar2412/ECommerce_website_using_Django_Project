from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.db import transaction
from django.core.paginator import Paginator
from decimal import Decimal
from .models import Order, OrderItem
from .forms import OrderForm
from reviews.models import Product


class OrderCreateView(LoginRequiredMixin, View):
    """Create a new order (checkout)"""
    template_name = 'orders/order_create.html'
    
    def get(self, request):
        form = OrderForm()
        return render(request, self.template_name, {'form': form, 'page_title': 'Checkout'})
    
    @transaction.atomic
    def post(self, request):
        form = OrderForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form, 'page_title': 'Checkout'})
        
        cart_items = request.session.get('cart', {})
        if not cart_items:
            messages.error(request, 'Your cart is empty.')
            return redirect('orders:create')
        
        subtotal = Decimal('0.00')
        items_data = []
        
        for product_id, item_data in cart_items.items():
            try:
                product = Product.objects.get(id=int(product_id))
                quantity = item_data.get('quantity', 1)
                price = product.discount_price if product.discount_price else product.price
                item_subtotal = price * quantity
                subtotal += item_subtotal
                items_data.append({
                    'product': product,
                    'quantity': quantity,
                    'price': price,
                    'subtotal': item_subtotal
                })
            except Product.DoesNotExist:
                continue
        
        if not items_data:
            messages.error(request, 'No valid items in cart.')
            return redirect('orders:create')
        
        tax = subtotal * Decimal('0.10')
        shipping_cost = Decimal('50.00')
        
        order = form.save(commit=False)
        order.user = request.user
        order.subtotal = subtotal
        order.tax = tax
        order.shipping_cost = shipping_cost
        order.save()
        
        for item in items_data:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['price'],
                subtotal=item['subtotal']
            )
        
        request.session['cart'] = {}
        messages.success(request, f'Order {order.order_number} created!')
        return redirect('orders:detail', order_id=order.id)


class OrderListView(LoginRequiredMixin, View):
    """List all orders (admin) or user's orders"""
    template_name = 'orders/order_list.html'
    
    def get(self, request):
        if request.user.is_staff:
            orders = Order.objects.all().order_by('-created_at')
        else:
            orders = Order.objects.filter(user=request.user).order_by('-created_at')
        
        paginator = Paginator(orders, 10)
        page_obj = paginator.get_page(request.GET.get('page'))
        
        return render(request, self.template_name, {'orders': page_obj, 'page_title': 'Orders'})


class OrderDetailView(LoginRequiredMixin, View):
    """Display order details"""
    template_name = 'orders/order_detail.html'
    
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        
        if not request.user.is_staff and order.user != request.user:
            messages.error(request, 'Permission denied.')
            return redirect('orders:list')
        
        return render(request, self.template_name, {
            'order': order,
            'order_items': order.items.all(),
            'page_title': f'Order {order.order_number}'
        })


class OrderSuccessView(LoginRequiredMixin, View):
    """Order success page"""
    template_name = 'orders/order_success.html'
    
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        return render(request, self.template_name, {'order': order, 'page_title': 'Order Success'})


@login_required
def cancel_order(request, order_id):
    """Cancel an order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status in ['cancelled', 'delivered', 'refunded']:
        messages.error(request, f'Cannot cancel order with status: {order.get_status_display()}')
        return redirect('orders:detail', order_id=order.id)
    
    if request.method == 'POST':
        order.status = 'cancelled'
        order.save()
        messages.success(request, f'Order {order.order_number} cancelled.')
        return redirect('orders:detail', order_id=order.id)
    
    return redirect('orders:detail', order_id=order.id)