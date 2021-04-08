from django.urls import path

from stock.views import StockListView, stock_update

app_name = 'stock'
urlpatterns = [
    path('update/', stock_update, name='stock_update'),
    path('', StockListView.as_view(), name='stock_list'),
]
