# likes/forms.py
from django import forms
from .models import Like
from blog.models import Post

class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = ['post']

    # Disable the form's post field since it will be passed in the view
    def __init__(self, *args, **kwargs):
        post = kwargs.pop('post', None)
        super().__init__(*args, **kwargs)
        if post:
            self.fields['post'].initial = post
