# likes/urls.py
from django.urls import path
from .views import *

app_name = 'likes'
urlpatterns = [

path('like/<int:post_id>/', LikePostView.as_view(), name='like_post'),
    path('favorite/<int:post_id>/', FavoritePostView.as_view(), name='favorite_post'),
    path('profile/favorites/', ProfileFavoritePostsView.as_view(), name='profile_favorites'),

]
