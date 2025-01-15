from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, Item
from .forms import OrderForm, StatusChangeForm, AddItemForm

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

@login_required
def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        form = StatusChangeForm(request.POST)
        if form.is_valid():
            order.status = form.cleaned_data['status']
            order.save()
            return redirect('order_list')
    else:
        form = StatusChangeForm(initial={'status': order.status})
    return render(request, 'orders/status_change_form.html', {'form': form, 'order_id': order.id})

@login_required
def add_item_to_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        form = AddItemForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data['item']
            quantity = form.cleaned_data['quantity']
            OrderItem.objects.create(order=order, item=item, quantity=quantity)
            return redirect('order_detail', order_id)
    else:
        form = AddItemForm()
    return render(request, 'orders/add_item_form.html', {'form': form, 'order_id': order_id})

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        order.delete()
        return redirect('order_list')
    return render(request, 'orders/delete_order_form.html', {'order': order})

@login_required
def search_orders(request):
    orders = Order.objects.all()
    search_query = request.GET.get('q', '')
    if search_query:
        orders = orders.filter(
            Q(table_number__icontains=search_query) |
            Q(status__icontains=search_query)
        )
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})