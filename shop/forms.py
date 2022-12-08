from django import forms
from shop.models import Order


class CartAddForm(forms.Form):
    amount = forms.IntegerField()


class OrderForm(forms.ModelForm):
    delivery_time = forms.DateTimeField(help_text='2022-10-25 14:30')

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'address', 'delivery_time', 'comment')
