from django.forms import ModelForm

from .models import Comment


class CommentForm(ModelForm):
    def __init__(self):
        super().__init__()

    class Meta:
        model = Comment
        fields = ['author', 'text']
