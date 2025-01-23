
from django import forms
from .models import Post, Category


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'category',  'published']  # Include the category field
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        }

        def save(self, user, commit=True):
            post = super().save(commit=False)
            post.author = user  # Set the current user as the author
            if commit:
                post.save()  # Save the instance to the database
            return post


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']