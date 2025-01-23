from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import *
from .forms import *
from blog.models import Post

#comment view
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        parent_comment = None

        # Check if this is a reply
        if 'parent_id' in self.request.POST:
            parent_comment = get_object_or_404(Comment, id=self.request.POST['parent_id'])

        form.instance.post = post
        form.instance.user = self.request.user
        form.instance.parent = parent_comment
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.kwargs['post_id']})
class PendingCommentsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Comment
    template_name = 'comments/pending_comments.html'
    context_object_name = 'comments'

    def get_queryset(self):
        # Show unapproved comments for posts owned by the current user or all if admin
        if self.request.user.is_superuser:
            return Comment.objects.filter(approved=False)
        return Comment.objects.filter(
            approved=False, post__author=self.request.user
        )

    def test_func(self):
        # Allow only admins or authors to view pending comments
        return self.request.user.is_superuser or Post.objects.filter(author=self.request.user).exists()
class ApproveCommentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = []  # No fields to edit in the form
    template_name = 'comments/approve_comment.html'

    def form_valid(self, form):
        comment = self.get_object()
        comment.approved = True
        comment.save()
        return redirect('comments:pending_comments')

    def test_func(self):
        comment = self.get_object()
        # Allow only admins or post authors to approve the comment
        return self.request.user.is_superuser or comment.post.author == self.request.user
class RejectCommentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comments/reject_comment.html'

    def get_success_url(self):
        return reverse_lazy('comments:pending_comments')

    def test_func(self):
        comment = self.get_object()
        # Allow only admins or post authors to reject the comment
        return self.request.user.is_superuser or comment.post.author == self.request.user


# like views
