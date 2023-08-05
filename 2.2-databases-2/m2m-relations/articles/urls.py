from django.urls import path

# from articles.views import articles_list
from articles.views import ArticleListView

urlpatterns = [
    path('', ArticleListView.as_view(), name='articles'),
]
