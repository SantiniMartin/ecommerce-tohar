from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.cart import Cart
from .models import Order, Payment, Cart as DBCart, ItemCart
from .forms import CheckoutForm
import uuid

@login_required
def checkout_view(request):
    cart = Cart(request)
    
    if len(cart) == 0:
        messages.warning(request, "Tu carrito está vacío. Agrega productos antes de pagar.")
        return redirect('cart:detail')
        
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # 1. Crear el carrito en BD para vincular a la orden (opcional, pero lo haremos segun modelo)
            db_cart, created = DBCart.objects.get_or_create(user=request.user)
            db_cart.empty_cart() # Limpiar iteraciones previas fallidas si existen
            
            for item in cart:
                ItemCart.objects.create(
                    cart=db_cart,
                    product=item['product'],
                    quantity=item['quantity']
                )
            
            # 2. Crear la orden
            order = Order.objects.create(
                user=request.user,
                cart=db_cart,
                status=Order.Status.COMPLETED,
                total_amount=cart.get_total_price()
            )
            
            # 3. Simular el pago
            Payment.objects.create(
                order=order,
                method=Payment.Method.CREDIT_CARD,
                amount=order.total_amount,
                status=Payment.Status.COMPLETED
            )
            
            # 4. Vaciar el carrito de la sesión
            cart.clear()
            
            # 5. Redirigir al éxito
            # Guardamos la orden en sesión para mostrar en success si queremos
            request.session['last_order_id'] = order.id
            messages.success(request, "¡Pago simulado exitoso!")
            return redirect('orders:success')
    else:
        form = CheckoutForm()
        
    context = {
        'cart': cart,
        'form': form,
        'total': cart.get_total_price(),
    }
    return render(request, 'orders/checkout.html', context)

@login_required
def payment_success_view(request):
    order_id = request.session.get('last_order_id')
    order = None
    if order_id:
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            pass
            
    return render(request, 'orders/success.html', {'order': order})
