from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название',
                             help_text='Напишите название сообщества')
    slug = models.SlugField(unique=True, verbose_name='Ссылка')
    description = models.TextField(verbose_name='Описание сообщества',
                                   help_text='Здесь напишите описание')

    class Meta:
        verbose_name = 'Сообщество'
        verbose_name_plural = 'Сообщества'

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name='Тест поста',
                            help_text='Здесь напишите текст вашего поста')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts',
                               verbose_name='Автор поста')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              blank=True, null=True, related_name='posts',
                              verbose_name='Сообщество',
                              help_text='Выберите сообщество')

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:15]
