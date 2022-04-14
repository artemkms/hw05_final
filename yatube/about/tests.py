from http import HTTPStatus

from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            "about/author.html": "/about/author/",
            "about/tech.html": "/about/tech/",
        }
        for template, adress in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertTemplateUsed(response, template)

    def test_urls_exists_at_desired_location(self):
        """Страницы, доступные любому пользователю."""
        urls = (
            "/about/author/",
            "/about/tech/",
        )
        for test_url in urls:
            response = self.guest_client.get(test_url)
            self.assertEqual(response.status_code, HTTPStatus.OK)
