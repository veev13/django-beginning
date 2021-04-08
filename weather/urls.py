from django.urls import path

from weather.views import WeatherListView, WeatherDetailView

app_name = 'weather'
urlpatterns = [
    path('', WeatherListView.as_view(), name='weather_list'),
    path('now/<int:pk>/', WeatherDetailView.as_view(), name='weather_detail'),
]
