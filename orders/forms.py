from django import forms
from .models import Order, Payment


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address']

        widgets = {
            'address': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your shipping address'}),
        }

class CheckoutForm(forms.Form):
    PAYMENT_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('crypto', 'Cryptocurrency'),
    ]
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect
    )
