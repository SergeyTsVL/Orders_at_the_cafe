from django.contrib.auth.models import User

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from .models import Order
from .forms import OrderForm

from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login, authenticate, logout


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
    order = Order.objects.get(pk=pk)
    if request.method == "POST":
        form = OrderForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            order.name = request.user
            form.save()
            print(type(order.status))
        if order.status == 'Оплачено':
            parts = order.description.split('\n')
            # print(parts)
            dictionaries = []
            for part in parts:
                dictionaries.append(part.split('-'))
            try:
                for i in dictionaries:
                    print(i, 1111111111111)
                    cleaned_list = [item.replace('\r', '') for item in i]
                    print(cleaned_list, 2222222222222222222)
                    # global REVENUE
                    order.revenue += int(cleaned_list[1]) * int(cleaned_list[2])
                    order.revenue.save()
                    # order.revenue = REVENUE
                    print(order.revenue, "order_editing")
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
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        order.delete()
        return redirect('/search')
    return render(request, 'orders/delete_order_form.html', {'order': order})

@login_required
def search_orders(request, price=0, revenue_1=0):
    orders = Order.objects.all()
    global REVENUE
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
                    order.revenue += float(int(cleaned_list[1]) * int(cleaned_list[2]))
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
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})




from django.contrib.postgres.search import SearchVector
from .forms import SearchForm

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Order.objects.annotate(search=SearchVector('title', 'body'),).filter(search=query)
    return render(request, 'orders/search_id.html', {'form': form, 'query': query, 'results': results})


