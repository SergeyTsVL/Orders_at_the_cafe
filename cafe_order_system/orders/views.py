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

# @login_required
# def update_order(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     if request.method == "POST":
#         form = StatusChangeForm(request.POST)
#         if form.is_valid():
#             order.status = form.cleaned_data['status']
#             order.save()
#             return redirect('order_list')
#     else:
#         form = StatusChangeForm(initial={'status': order.status})
#     return render(request, 'orders/status_change_form.html', {'form': form, 'order_id': order.id})

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
def search_orders(request, description_list = [], price_list = []):
    orders = Order.objects.all()
    # global description_list
    # global price_list
    price_list = []
    for order in orders:
        description_list.append(order.description)
        price_list.append(order.price)
    total_price_list = sum(price_list)
        # print(price_list)
    # description_list = []

        # order.description
        # order.price = list(order.price)
    # search_query = request.GET.get('q', '')description_list = []
    # price_list = []
    # if search_query:
    #     orders = orders.filter(
    #         Q(table_number__icontains=search_query) |
    #         Q(status__icontains=search_query)
    #     )
    return render(request, 'orders/order_list.html', {'orders': orders, 'price_list': price_list,
                                                      'total_price_list': total_price_list})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})