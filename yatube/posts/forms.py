from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group']
        labels = {'text': 'Текст записи', 'group': 'Сообщество'}
        widgets = {'text': forms.Textarea()}
        help_texts = {'text': 'Здесь напишите свой пост',
                      'group': 'Выберите сообщество'}
