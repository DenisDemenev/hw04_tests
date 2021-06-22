from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from posts.models import Post, Group

User = get_user_model()


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_home(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_author(self):
        response = self.guest_client.get('/author')
        self.assertEqual(response.status_code, 200)

    def test_tech(self):
        response = self.guest_client.get('/tech')
        self.assertEqual(response.status_code, 200)


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Post.objects.create(
            text='Тестовый текст',
            id='189'
        )
        super().setUpClass()
        Group.objects.create(
            title='Тестовая группа',
            slug='slug-test',
            description='Тестовое описание сообщества'
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='DenisD')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_uses_template(self):
        templates_url_names = {
            'templates/index.html': '/',
            'templates/group.html': 'group/slug-test/',
            'templates/new.html': 'new/',
            'templates/post.html': 'DenisD/189',
            'templates/profile.html': 'DenisD/',
        }
        for template, adress in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)

            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertTemplateUsed(response, template)
