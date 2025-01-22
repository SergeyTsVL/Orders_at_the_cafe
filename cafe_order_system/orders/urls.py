from django.urls import path, include
from .views import create_order, delete_order, search_orders, order_detail, home, \
    logout_view, signup, order_editing, post_search, no_number, revenue_volume, index


urlpatterns = [
    path('create/', create_order, name='create_order'),
    path('no_number/', no_number, name='no_number'),
    path('revenue_volume/', revenue_volume, name='revenue_volume'),
    path('order/edit/<int:pk>/', order_editing, name='editing_order'),
    path('delete/<int:order_id>/', delete_order, name='delete_order'),
    path('search/', search_orders, name='search_orders'),
    path('detail/<int:order_id>/', order_detail, name='order_detail'),
    path('', home, name='home'),
    path('accounts/logout/', logout_view, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', signup, name='signup'),
    path('search_id/', post_search, name='post_search'),
]
