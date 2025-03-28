from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from shop.models import Product


# Create your models here.
class Order(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = PhoneNumberField(region='RU')
    postal_code = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    delivery_type = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.name
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return self.product.name
    def get_total(self):
        return  self.price * self.quantity



