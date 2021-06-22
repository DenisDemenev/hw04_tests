from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Post, Group

User = get_user_model()


class PostsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='DenisD')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            description='Описание',
            slug='test-slug',
        )

        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
        )

        cls.post_two = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.form_fields_new_post = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        self.pages_with_posts = [
            reverse('index'),
            reverse('group_posts', kwargs={'slug': 'test-slug'})
        ]

    def test_pages_correct_template(self):
        templates_page_names = {
            'posts/index.html': reverse('index'),
            'posts/new_post.html': reverse('new_post'),
            'posts/group.html': reverse('group_posts',
                                        kwargs={'slug': 'test-slug'}),
        }
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_home_page_show_correct_context(self):
        response = self.guest_client.get(reverse('index'))
        self.assertEqual(response.context.get('page').object_list[-1],
                         self.post)

    def test_group_page_correct_context(self):
        response = self.guest_client.get(reverse(
            'group_posts', kwargs={'slug': 'test-slug'}
        ))
        self.assertEqual(response.context['group'], self.group)
        self.assertEqual(response.context.get('page').object_list[-1],
                         self.post_two)

    def test_new_page_context(self):
        response = self.authorized_client.get(reverse('new_post'))
        for value, expected in self.form_fields_new_post.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_group_pages_not_new_post(self):
        response = self.authorized_client.get(
            reverse('group_posts', kwargs={'slug': 'test-slug'}))
        self.assertTrue(self.post not in response.context['page'])

    def test_page_not_found(self):
        response_page_not_found = self.guest_client.get('/tests_url/')
        self.assertEqual(response_page_not_found.status_code, 404)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Test User')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        for count in range(13):
            cls.post = Post.objects.create(
                text=f'Тестовый пост номер {count}',
                author=cls.user)

    def test_first_page_contains_ten_records(self):
        response = self.authorized_client.get(reverse('index'))
        self.assertEqual(len(response.context.get('page').object_list), 10)

    def test_second_page_contains_three_records(self):
        response = self.authorized_client.get(
            reverse('index') + '?page=2'
        )
        self.assertEqual(len(response.context.get('page').object_list), 3)
