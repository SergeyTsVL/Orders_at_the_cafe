from django import forms
from .models import Order, Item, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number', 'items']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['items'].widget = forms.CheckboxSelectMultiple()
        self.fields['items'].queryset = Item.objects.all()

class StatusChangeForm(forms.Form):
    status = forms.ChoiceField(choices=Order.STATUS_CHOICES)

class AddItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['item', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.all()


