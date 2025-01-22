from django.urls import path, include
from .views import create_order, delete_order, search_orders, order_detail, home, \
    logout_view, signup, order_editing, post_search

# app_name = 'orders'

urlpatterns = [
    path('create/', create_order, name='create_order'),
    # path('order_form/', order_editing, name='editing_order'),
    path('order/edit/<int:pk>/', order_editing, name='editing_order'),
    # path('update/<int:order_id>/', update_order, name='update_order'),
    # path('add-item/<int:order_id>/', add_item_to_order, name='add_item_to_order'),
    path('delete/<int:order_id>/', delete_order, name='delete_order'),
    path('search/', search_orders, name='search_orders'),
    path('detail/<int:order_id>/', order_detail, name='order_detail'),
    path('', home, name='home'),
    path('accounts/logout/', logout_view, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', signup, name='signup'),
    # path('', include('orders.urls')),
    path('search/', post_search, name='post_search'),
]
