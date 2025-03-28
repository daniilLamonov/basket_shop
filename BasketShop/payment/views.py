import uuid

from django.conf import settings
from django.shortcuts import redirect, get_object_or_404, render
from yookassa import Configuration, Payment

from orders.models import Order

Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


def create_payment(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, pk=order_id)
    amount = sum(item.get_total() for item in order.items.all()) # Сумма платежа, полученная из корзины
    payment_id = str(uuid.uuid4())  # Уникальный идентификатор платежа
    payment = Payment.create({
        "amount": {
            "value": amount,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "http://127.0.0.1:8000/payment/success/"
        },
        "capture": True,
        "description": f'Оплата заказа № {order_id} для {order.email}',
        "receipt": {
            "customer": {
                "email": order.email
            },
            "items": [
                {
                    "description": item.product.name,
                    "amount": {
                        "value": str(item.price),
                        "currency": "RUB"
                    },
                    "vat_code": 20,
                    "quantity": item.quantity
                }
                for item in order.items.all()
            ]
        }
    })

    confirmation_url = payment.confirmation.confirmation_url
    return redirect(confirmation_url)
def payment_success(request):
    return render(request, 'payment/payment_success.html', {})