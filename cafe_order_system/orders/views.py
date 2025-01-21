from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order
from .forms import OrderForm

from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login, authenticate, logout


# description_list = []
# price_list = []

def logout_view(request):
    """
    Этот метод выполняет выход пользователя из системы и перенаправляет его на домашнюю страницу.
    """
    logout(request)
    return redirect('home')

def signup(request):
    """
    Вызывает страницу для подписи объявлений.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def home(request):
    """
    Вызывает страницу home.html.
    """
    return render(request, 'home.html')

@login_required
def create_order(request):

    if request.method == "POST":
        form = OrderForm(request.POST)

        if form.is_valid():
            order = form.save()

            return redirect('order_detail', order.id)
    else:
        form = OrderForm()
    return render(request, 'orders/order_form.html', {'form': form})
    # if request.method == "POST":



# def string_to_nested_dict(text):
#     parts = text.split('\n')
#     dictionaries = []
#     for part in parts:
#         if ';' in part:
#             inner_dict = dict(pair.split('=') for pair in part.split(';'))
#             dictionaries.append(inner_dict)
#         else:
#             dictionaries.append({part.split('=')[0]: part.split('=')[1]})
#
#     return {i: inner_dict for i, inner_dict in enumerate(dictionaries)}
#
#
# # Пример использования
# text = "key1=value1;key2=value2\nkeyA=valueA\nkeyB=valueB"
# result = string_to_nested_dict(text)
# print(result)





# @login_required
# def order_editing(request, pk):
#     order = Order.objects.get(pk=pk)
#     if request.method == "POST":
#         form = OrderForm(request.POST, request.FILES, instance=order)
#         if form.is_valid():
#             order.name = request.user
#             form.save()
#
#             return redirect('orders:editing_order', pk=pk)
#     else:
#         # вызов функции которая отобразит в браузере указанный шаблон с данными формы и объявления.
#         form = OrderForm(instance=order)
#     return render(request, 'orders/editing_order.html',
#                   {'form': form, 'order': order})




    # order = get_object_or_404(Order, id=order_id)
    # if request.method == "POST":
    #     form = StatusChangeForm(request.POST)
    #     if form.is_valid():
    #         order.status = form.cleaned_data['status']
    #         order.save()
    #         return redirect('order_list')
    # else:
    #     form = StatusChangeForm(initial={'status': order.status})
    # return render(request, 'orders/status_change_form.html', {'form': form, 'order_id': order.id})

# @login_required    # Проверяет регистрацию пользователя
# def edit_advertisement(request, pk):

#     advertisement = Advertisement.objects.get(pk=pk)
#     if advertisement.status != 'товар передан в доставку' and advertisement.status != 'товар доставлен':
#         if request.method == "POST":
#             form = AdvertisementForm(request.POST, request.FILES, instance=advertisement)
#
#             if form.is_valid():
#                 advertisement.name = request.user
#
#                 advertisement.status = 'заявка создана'
#                 form.save()
#                 img_obj = form.instance
#                 # Перенаправляет на страницу с сохраненными исправлениями.
#                 return redirect('board:advertisement_detail', pk=img_obj.pk)
#         else:
#             # вызов функции которая отобразит в браузере указанный шаблон с данными формы и объявления.
#             form = AdvertisementForm(instance=advertisement)
#         return render(request, 'board/edit_advertisement.html',
#                       {'form': form, 'advertisement': advertisement})
#     return redirect('board:advertisement_detail', pk=pk)





# @login_required
# def add_item_to_order(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     if request.method == "POST":
#         form = AddItemForm(request.POST)
#         if form.is_valid():
#             item = form.cleaned_data['item']
#             quantity = form.cleaned_data['quantity']
#             OrderItem.objects.create(order=order, item=item, quantity=quantity)
#             return redirect('order_detail', order_id)
#     else:
#         form = AddItemForm()
#     return render(request, 'orders/add_item_form.html', {'form': form, 'order_id': order_id})

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        order.delete()
        return redirect('order_list')
    return render(request, 'orders/delete_order_form.html', {'order': order})

@login_required
def search_orders(request, description_list=[], price = 0):
    orders = Order.objects.all()
    price_list = []


    for order in orders:
        parts = order.description.split('\n')
        dictionaries = []
        for part in parts:
            dictionaries.append(part.split('-'))
        try:
            for i in dictionaries:
                cleaned_list = [item.replace('\r', '') for item in i]
                price += int(cleaned_list[1]) * int(cleaned_list[2])
        except:
            price = None
        order.price = price
        price_list.append(order.price)
        price = 0
    try:
        total_price_list = sum(price_list)
    except:
        total_price_list = "не корректно введена цена"

    return render(request, 'orders/order_list.html', {'orders': orders, 'price_list': price_list,
                                                      'total_price_list': total_price_list, 'price': price})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})


