# blog/urls.py
from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('category/new/', CategoryCreateView.as_view(), name='category_create'),
    path("search/", TaskSearchView.as_view(), name="post_search"),

]
