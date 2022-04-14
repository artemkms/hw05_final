from django import forms
from django.forms import models

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("text", "group", "image")
        help_texts = {
            "text": "Текст нового поста",
            "group": "Группа, к которой будет относиться пост",
        }
        labels = {
            "text": "Текст поста",
            "group": "Группа",
        }


class CommentForm(models.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
