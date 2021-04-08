from django.urls import path, include

from restapi.views import NewsViewSet, StockViewSet, NowWeatherViewSet

app_name = 'restapi'
news_list = NewsViewSet.as_view({
    'get': 'list'})
stock_list = StockViewSet.as_view({
    'get': 'list',
    'post': 'create', })
stock_detail = StockViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy', })
weather_list = NowWeatherViewSet.as_view({
    'get': 'list',
})
urlpatterns = [
    # DEBUG: 'auth/login/ 에서 rest_framework를 찾을 수 없다는 오류 발생
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('newses/', news_list, name='news_list'),
    path('stocks/', stock_list, name='stock_list'),
    path('stocks/<str:pk>', stock_detail, name='stock_detail'),
    path('weathers/', weather_list, name='weather_list'),
]
