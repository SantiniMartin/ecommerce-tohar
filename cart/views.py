from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from products.models import Product 
from .cart import Cart

# Detalle del carrito

def cart_detail(request):
    """Muestra el contenido actual del carrito."""
    cart = Cart(request)
    context = {
        'cart': cart,
        'total': cart.get_total_price(),
    }
    return render(request, 'cart/cart_detail.html', context)


# Añadir producto

@require_POST
def cart_add(request, product_id):
    """
    Añade un producto al carrito.
    Acepta los parámetros POST:
        - quantity  (int, default 1)
        - override  ('true' para reemplazar la cantidad, 'false' para sumar)
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1

    override = request.POST.get('override', 'false').lower() == 'true'

    if quantity < 1:
        messages.warning(request, "La cantidad debe ser al menos 1.")
        return redirect('cart:detail')

    if quantity > product.stock:
        messages.warning(
            request,
            f"Solo hay {product.stock} unidades disponibles de «{product.name}»."
        )
        quantity = product.stock

    cart.add(product=product, quantity=quantity, override_quantity=override)
    messages.success(request, f"«{product.name}» agregado al carrito.")

    # Redirigir a la página de origen en lugar del carrito
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
    return redirect('home')


# Eliminar producto

@require_POST
def cart_remove(request, product_id):
    """Elimina un producto del carrito."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f"«{product.name}» eliminado del carrito.")
    return redirect('cart:detail')


# Vaciar carrito

@require_POST
def cart_clear(request):
    """Vacía el carrito por completo."""
    cart = Cart(request)
    cart.clear()
    messages.info(request, "El carrito fue vaciado.")
    return redirect('cart:detail')