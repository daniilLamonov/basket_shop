from decimal import Decimal

from django.conf import settings
from django.contrib.sites import requests

from shop.models import Product


class Cart():
    def __init__(self, request):
        self.session=request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    def save(self):
        self.session.modified = True
    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity,
                                     'price': str(product.price)}
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    def __iter__(self):
        products_ids = self.cart.keys()
        products = Product.objects.filter(id__in=products_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    def __len__(self):
        return sum(item for item in self.cart.values())
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def serialize(self):
        """
        Сериализация данных корзины в формат, который можно передать в JSON.
        """
        serialized_cart = []
        for item in self:
            serialized_cart.append({
                'product_id': item['product'].id,
                'product_name': item['product'].name,
                'quantity': item['quantity'],
                'price': str(item['price']),  # Преобразуем Decimal в строку
                'total_price': str(item['total_price'])  # Преобразуем Decimal в строку
            })
        return serialized_cart