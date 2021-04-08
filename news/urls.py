from django.urls import path

from news.views import NewsListView, crawl_news

app_name = 'news'
urlpatterns = [
    # news list
    path('', NewsListView.as_view(), name='news_list'),
    path('update/', crawl_news, name='news_crawl'),
]
