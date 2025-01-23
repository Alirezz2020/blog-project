from django.urls import path
from .views import *

app_name = 'comments'

urlpatterns = [
    path('post/<int:post_id>/add/', CommentCreateView.as_view(), name='add_comment'),
    path('pending/', PendingCommentsListView.as_view(), name='pending_comments'),
    path('<int:pk>/approve/', ApproveCommentView.as_view(), name='approve_comment'),
    path('<int:pk>/reject/', RejectCommentView.as_view(), name='reject_comment'),

]
