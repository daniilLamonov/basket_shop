from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import Order


DELIVERY_CHOICES = [
        ('standard', 'Стандартная доставка'),
        ('express', 'Экспресс-доставка'),
        ('pickup', 'Самовывоз'),
    ]

class OrderForm(forms.ModelForm):
    delivery_type = forms.ChoiceField(
        choices=DELIVERY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Способ доставки"
    )
    phone = PhoneNumberField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите телефон', 'value': '+7'}),
        label='Телефон'
        )
    class Meta:
        model = Order
        fields = ['name', 'email', 'phone', 'postal_code', 'country', 'city', 'address', 'delivery_type']
        labels = {
            'name': 'Ваше имя',
            'email': 'Электронная почта',
            'phone': 'Телефон',
            'postal_code': 'Почтовый индекс',
            'country': 'Страна',
            'city': 'Город',
            'address': 'Адрес доставки',
            'delivery_type': 'Способ доставки'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваше имя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите email'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш почтовый индекс'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите вашу страну'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш город'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите улицу и дом'}),
        }