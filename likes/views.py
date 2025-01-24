
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from blog.models import Post
from .models import Like, Favorite

class LikePostView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        # Check if the user has already liked the post
        existing_like = Like.objects.filter(user=request.user, post=post).first()

        if existing_like:
            # If the user has already liked the post, remove the like (unlike)
            existing_like.delete()
        else:
            # If the user hasn't liked the post, create a like
            Like.objects.create(user=request.user, post=post)

        return redirect('blog:post_list')  # Redirect back to the post list page
class FavoritePostView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        # Check if the user has already added the post to favorites
        existing_favorite = Favorite.objects.filter(user=request.user, post=post).first()

        if existing_favorite:
            # If the user has already favorited the post, remove it (unfavorite)
            existing_favorite.delete()
        else:
            # If the user hasn't favorited the post, add it to favorites
            Favorite.objects.create(user=request.user, post=post)

        return redirect('blog:post_list')  # Redirect back to the post list page
class ProfileFavoritePostsView(LoginRequiredMixin, TemplateView):
    template_name = 'likes/favorite_posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the logged-in user
        user = self.request.user
        # Get all the posts favorited by this user
        favorite_posts = Post.objects.filter(favorites__user=user)
        context['favorite_posts'] = favorite_posts
        return context


