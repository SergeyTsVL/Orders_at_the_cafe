from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Order
from .forms import OrderForm

from .forms import SignUpForm
from django.contrib.auth import login, logout
from .forms import SearchForm


REVENUE = 0   # Выручка за сессию

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
    """
    Создает заказ, при этом контролирует чтобы все поля были заполнены.
    """
    if request.method == "POST":
        form = OrderForm(request.POST)
        if (form.is_valid() and form['table_number'].value() != '' and form['description'].value() != ''
                and form['name'].value() != ''):
            # print(form['description'].value())
            order = form.save()
            return redirect('order_detail', order.id)
    else:
        form = OrderForm()
    return render(request, 'orders/order_form.html', {'form': form})

@login_required
def order_editing(request, pk):
    """
    Редактирует заказ, определяет стоимость заказа.
    """
    order = Order.objects.get(pk=pk)
    if request.method == "POST":
        form = OrderForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            order.name = request.user
            form.save()
        if order.status == 'Оплачено':
            parts = order.description.split('\n')
            dictionaries = []
            for part in parts:
                dictionaries.append(part.split('-'))
            try:
                for i in dictionaries:
                    cleaned_list = [item.replace('\r', '') for item in i]
                    order.revenue += int(cleaned_list[1]) * int(cleaned_list[2])
                    order.revenue.save()
            except:
                print('Не корректное отображение выручки')

            return redirect('/search')
    else:
        # вызов функции которая отобразит в браузере указанный шаблон с данными формы и объявления.
        form = OrderForm(instance=order)
    return render(request, 'orders/editing_order.html',
                  {'form': form, 'order': order})

@login_required
def delete_order(request, order_id):
    """
    Удаляет заказ из базы данных.
    """
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        order.delete()
        return redirect('/search')
    return render(request, 'orders/delete_order_form.html', {'order': order})

@login_required
def search_orders(request, price=0, revenue_1=0):
    """
    Отображает список всех заказов, рассчитывает стоимость заказов и дневную выручку.
    """
    orders = Order.objects.all()

    # paginator = Paginator(orders, 4)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    price_list = []
    for order in orders:
        order.revenue = 0
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
        price_list.append(price)
        price = 0
        if order.status == 'Оплачено':
            parts = order.description.split('\n')
            dictionaries = []
            for part in parts:
                dictionaries.append(part.split('-'))
            try:
                for i in dictionaries:
                    cleaned_list = [item.replace('\r', '') for item in i]
                    order.revenue = float(int(cleaned_list[1]) * int(cleaned_list[2]))
                    revenue_1 += order.revenue
            except:
                print('Не корректное отображение выручки')
    try:
        total_price_list = sum(price_list)
    except:
        total_price_list = "не корректно введена цена"
    return render(request, 'orders/order_list.html', {'orders': orders, 'price_list': price_list,
                                          'total_price_list': total_price_list, 'price': price, 'REVENUE': revenue_1})

@login_required
def order_detail(request, order_id):
    """
    Отображает искомый или созданный заказ, если стол удален или нет заказа с таким номером открывает
    представление с оповещением об этом.
    """
    try:
        order = get_object_or_404(Order, table_number=order_id)
    except:
        return redirect('/')
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def no_number(request):
    orders = Order.objects.all()
    return render(request, 'orders/no_number.html', {'orders': orders})

@login_required
def post_search(request):
    """
    Создает строчку для поиска заказа по номеру стола.
    """
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            return redirect(f'/detail/{query}/')
    return render(request, 'orders/search_id.html', {'form': form, 'query': query, 'results': results})


def revenue_volume(request, price_list=[], revenue_1=0):
    """
    Рассчитывает и отображает выручку с не удаленных заказов со статусом "оплачено".
    """
    orders = Order.objects.all()
    for order in orders:
        print(order.revenue)
        price = order.price
        price_list.append(price)
        price = 0
        if order.status == 'Оплачено':
            parts = order.description.split('\n')
            dictionaries = []
            for part in parts:
                dictionaries.append(part.split('-'))
            try:
                for i in dictionaries:
                    cleaned_list = [item.replace('\r', '') for item in i]
                    order.revenue = float(int(cleaned_list[1]) * int(cleaned_list[2]))
                    revenue_1 += order.revenue
            except:
                print('Не корректное отображение выручки')
    return render(request, 'orders/revenue_volume.html', {'orders': orders,
                                'price_list': price_list, 'REVENUE': revenue_1})

