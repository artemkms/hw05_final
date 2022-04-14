from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_author = User.objects.create(username="HasNoName")
        cls.test_post = Post.objects.create(
            text="Текст поста",
            pub_date="12.10.2021",
            author=cls.test_author,
            group=Group.objects.create(
                title="ЗаголовокГруппы",
                slug="test_slug",
                description="ТестовоеОписание",
            ),
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client_author = Client()
        self.authorized_client_author.force_login(self.test_author)
        self.not_author = User.objects.create(username="NotAuthor")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.not_author)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
         templates_url_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:profile',
                    args=[self.test_author.username]):
            'posts/profile.html',
            reverse('posts:post_detail', args=[self.test_post.id]):
            'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create.html',
            reverse('posts:post_edit', args=[self.test_post.id]):
            'posts/create.html',
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client_author.get(adress)
                self.assertTemplateUsed(response, template)

    def test_urls_exists_at_desired_location(self):
        """Страницы, доступные любому пользователю."""
        urls = (
            reverse('posts:index'),
            reverse('posts:profile',
                    args=[self.test_author.username]),
            reverse('posts:post_detail',
                    args=[self.test_post.id]),
            "/unexisting_page/",
        )
        for test_url in urls:
            response = self.guest_client.get(test_url)
            if test_url == "/unexisting_page/":
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
            else:
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_url_exists_at_desired_location_authorized(self):
        """Страница 'create' доступна авторизованному пользователю."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_url_redirect_anonymous(self):
        """Страница 'create' перенаправляет анонимного пользователя."""
        response = self.guest_client.get(reverse('posts:post_create'), follow=True)
        self.assertRedirects(response, "/auth/login/?next=/create/")

    def test_edit_url_redirect_non_author(self):
        """
        Страница 'edit' перенаправляет зарегистрированного
        пользователя (не автора поста).
        """
        response = self.authorized_client.get(
            reverse('posts:post_create'), follow=True
        )
        self.assertRedirects(
            response, reverse('posts:post_detail', args=[self.test_post.id])
            )
