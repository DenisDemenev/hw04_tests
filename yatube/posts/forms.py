from django import forms
from django.db import models

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group', 'image']
        labels = {'text': 'Текст записи', 'group': 'Сообщество',
                  'image': 'Картинка'}
        widgets = {'text': forms.Textarea()}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {'text': forms.Textarea()}