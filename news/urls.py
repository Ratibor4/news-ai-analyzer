from django.urls import path
from . import views

urlpatterns = [
    path("", views.news_list, name="news_list"),
    path("latest/", views.latest_news_page, name="latest_news"),
    path("fetch-latest/", views.fetch_latest_news, name="fetch_latest_news"),
]




