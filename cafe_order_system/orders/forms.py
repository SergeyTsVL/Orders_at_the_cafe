from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number', 'name', 'description', 'price', 'status']


class SignUpForm(UserCreationForm):
    """
    Этот класс SignUpForm представляет собой кастомную форму регистрации пользователя, которая расширяет стандартную
    форму UserCreationForm. UserCreationForm - Это стандартная форма Django для регистрации новых пользователей.
    SignUpForm расширяет UserCreationForm, что позволяет переопределить некоторые аспекты формы, если необходимо.
    Использование Meta позволяет задать метаданные формы без необходимости создавать отдельный экземпляр класса.
    Поле fields определяет, какие поля формы будут отображаться. В данном случае это базовые поля для регистрации
    пользователя.
    """
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',)


# from django import forms
# from .models import Item, Order, OrderItem
#
#
# class ItemForm(forms.ModelForm):
#     class Meta:
#         model = Item
#         fields = ['name', 'description', 'price']
#
#
# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['table_number', 'status']
#
#
# class OrderItemForm(forms.ModelForm):
#     class Meta:
#         model = OrderItem
#         fields = ['item', 'quantity']
#
#
# # Форма для добавления новых товаров в заказ
# class AddToOrderForm(forms.Form):
#     item_id = forms.IntegerField(widget=forms.HiddenInput())
#     quantity = forms.IntegerField(min_value=1, widget=forms.HiddenInput())
#
#
# def create_order_form(request):
#     if request.method == 'POST':
#         form = AddToOrderForm(request.POST)
#         if form.is_valid():
#             item_id = form.cleaned_data['item_id']
#             quantity = form.cleaned_data['quantity']
#
#             # Получаем товар по ID
#             item = Item.objects.get(id=item_id)
#
#             # Создаем новую запись OrderItem
#             OrderItem.objects.create(
#                 order=request.user.current_order,
#                 item=item,
#                 quantity=quantity
#             )
#
#             # Обновляем общую сумму заказа
#             request.user.current_order.update_total()
#
#             # Обновляем страницу без перезагрузки
#             return HttpResponse(status=200)
#     else:
#         form = AddToOrderForm()
#
#     return render(request, 'add_item_to_order.html', {'form': form})