from decimal import Decimal
from django.conf import settings
from products.models import Product  # Ajustá 'store' al nombre de tu app

CART_SESSION_ID = 'cart'


class Cart:
    """
    Carrito de compras basado en sesiones.
    Cada ítem se almacena como:
        {
            'product_id': {
                'quantity': int,
                'price': str,          # price original
                'final_price': str,    # price con descuento aplicado
            }
        }
    """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    # ------------------------------------------------------------------
    # Persistencia
    # ------------------------------------------------------------------

    def save(self):
        """Marca la sesión como modificada para forzar el guardado."""
        self.session.modified = True

    # ------------------------------------------------------------------
    # Operaciones principales
    # ------------------------------------------------------------------

    def add(self, product, quantity=1, override_quantity=False):
        """
        Añade un producto al carrito o actualiza su cantidad.

        Args:
            product: instancia de Product.
            quantity: cantidad a añadir (int).
            override_quantity: si True, reemplaza la cantidad en lugar de sumarla.
        """
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),
                'final_price': str(product.final_price),
                'discount_percentage': product.discount_percentage,
            }

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        # Respeta el stock disponible
        self.cart[product_id]['quantity'] = min(
            self.cart[product_id]['quantity'],
            product.stock,
        )

        self.save()

    def remove(self, product):
        """Elimina un producto del carrito por completo."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """Vacía el carrito eliminando la clave de sesión."""
        del self.session[CART_SESSION_ID]
        self.save()

    # ------------------------------------------------------------------
    # Consultas / cálculos
    # ------------------------------------------------------------------

    def __iter__(self):
        """
        Itera sobre los ítems del carrito enriqueciendo cada uno
        con la instancia del Product y el subtotal calculado.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        product_map = {str(p.id): p for p in products}

        cart_copy = dict(self.cart)  # copia para no mutar la sesión al iterar

        for product_id, item in cart_copy.items():
            item['product'] = product_map.get(product_id)
            item['final_price'] = Decimal(item['final_price'])
            item['total_price'] = item['final_price'] * item['quantity']
            yield item

    def __len__(self):
        """Devuelve la cantidad total de unidades en el carrito."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Devuelve el precio total del carrito como Decimal."""
        return sum(
            Decimal(item['final_price']) * item['quantity']
            for item in self.cart.values()
        )

    def get_item_count(self):
        """Alias explícito para usar en templates/context processors."""
        return len(self)