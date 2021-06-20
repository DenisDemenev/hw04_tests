from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, Group

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Post.objects.create(
            text='Тестовый пост',
            id='189',
        )
        super().setUpClass()
        Group.objects.create(
            title='Тестовая группа',
            slug='slug-test',
            description='Тестовое описание',
        )

    def setUp(self):
        self.user = User.objects.create_user(username='DenisD')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_use_correct_template(self):
        templates_pages_names = {
            'templates/index.html': reverse('posts:index'),
            'templates/group.html': (
                reverse('posts: group_posts', kwargs={'slug': 'slug-test'})),
            'templates/posts/new.html': reverse('posts:new_post'),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template) 