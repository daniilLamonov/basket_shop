from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import OrderForm
from .models import OrderItem
from cart.cart import Cart



# Create your views here.

def create_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save()
            # total_price = cart.get_total_price()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         quantity=item['quantity'],
                                         price=item['price'])
            cart.clear()
            request.session['order_id'] = order.id
            return redirect(reverse('payment:pay'))
        else:
            print(form.errors)
    else:
        form = OrderForm(request.POST, request.FILES)
    return render(request, 'orders/create_order.html', {'form': form})

