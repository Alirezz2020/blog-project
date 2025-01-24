
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Category
from .forms import PostForm, CategoryForm
from comments.models import Comment
from taggit.models import Tag

from likes.forms import LikeForm
from likes.models import Like



class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 3  # Number of tasks per page


    def get_queryset(self):
        queryset = Post.objects.filter(published=True).order_by('-created_at')

        tag = self.request.GET.get('tag')

        if tag:
            queryset = queryset.filter(tags__name__icontains=tag)

        # Get filter parameters
        author_id = self.request.GET.get('author')
        category_id = self.request.GET.get('category')
        tag_id = self.request.GET.get('tag')


        # Apply filters
        if author_id:
            queryset = queryset.filter(author__id=author_id)
        if category_id:
            queryset = queryset.filter(category__id=category_id)
            if tag_id:
                queryset = queryset.filter(tags__id=tag_id)



        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        posts = self.get_queryset()
        page_number = self.request.GET.get('page', 1)  # Get current page, default to 1
        paginator = Paginator(posts, self.paginate_by)  # Paginate the filtered tasks
        current_page = paginator.get_page(page_number)

        for post in context['posts']:
            post.like_count = post.likes.count()  # Add like count to each post
            post.favorite_count = post.favorites.count()  # Add favorite count to each post

        context['current_page'] = current_page.number
        context['total_pages'] = paginator.num_pages
        context['authors'] = User.objects.all()
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()  # Fetch all available tags
        context['filters'] = {
            'author': self.request.GET.get('author', ''),
            'category': self.request.GET.get('category', ''),
            'tag': self.request.GET.get('tag', ''),  # Add current tag filter

        }

        return context
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        # Get the user making the request
        user = self.request.user

        # Filter comments: show all approved comments or user's own comments
        comments = Comment.objects.filter(post=post, parent__isnull=True).filter(approved=True) | \
                  Comment.objects.filter(post=post, parent__isnull=True, user=user)

        # Paginate comments (5 per page)
        paginator = Paginator(comments, 5)  # 5 comments per page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Get replies: show all replies (regardless of approval)
        replies = Comment.objects.filter(post=post, parent__isnull=False)

        # Paginate replies (5 per page, or set a different number)
        replies_paginator = Paginator(replies, 5)
        replies_page_number = self.request.GET.get('replies_page')
        replies_page_obj = replies_paginator.get_page(replies_page_number)

        context['comments'] = page_obj
        context['replies'] = replies_page_obj
        context['page_obj'] = page_obj  # for pagination controls of comments
        context['replies_page_obj'] = replies_page_obj  # for pagination controls of replies

        return context
class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        # Set the author field to the current logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)
class PostUpdateView(LoginRequiredMixin,UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('accounts:profile')
class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('accounts:profile')
class CategoryCreateView(LoginRequiredMixin,CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'blog/category_form.html'
    success_url = reverse_lazy('blog:post_list')


class TaskSearchView(ListView):
    model = Post
    template_name = "blog/task_search_results.html"
    context_object_name = "posts"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query), )
        return Post.objects.none()