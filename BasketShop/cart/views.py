from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from .cart import Cart
from shop.models import Product


# Create your views here.
def get_cart(request):
    cart = Cart(request)
    data = cart.serialize()

    # cart_data = list(cart)
    return JsonResponse({'cart': data})

@require_POST
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)
    return JsonResponse({'cartCount': str(len(cart))})

@require_POST
def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return JsonResponse({'success': True, 'cartCount': str(len(cart))})