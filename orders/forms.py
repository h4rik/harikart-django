from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order  # Order table in models.py
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'city', 'state', 'country',  'order_note', ]
