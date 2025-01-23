from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from blog.models import Post

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    created_at = models.DateTimeField(default=now)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post}'

    class Meta:
        ordering = ['-created_at']

