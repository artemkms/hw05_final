import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Comment, Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_author = User.objects.create(username="PostAuthor")
        cls.group = Group.objects.create(
            title="ЗаголовокГруппы",
            slug="test_slug",
            description="ТестовоеОписание",
        )
        cls.test_post = Post.objects.create(
            text="Текст поста", author=cls.test_author, group=cls.group
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.test_author)

    def test_create_post(self):
        """Валидная форма создает новый Post"""
        posts_count = Post.objects.count()
        form_data = {
            "text": "Текст нового поста",
            "group": self.group.id,
        }
        response = self.authorized_client.post(
            reverse("posts:post_create"), data=form_data, follow=True
        )
        self.assertRedirects(
            response,
            reverse(
                "posts:profile",
                kwargs={"username": self.test_author.username}
            ),
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        new_post = Post.objects.all()[0]
        self.assertEqual(new_post.text, form_data["text"])
        self.assertEqual(new_post.group.id, form_data["group"])
        self.assertEqual(new_post.author, self.test_author)

    def test_edit_post(self):
        """Валидная форма изменяет существующий Post"""
        posts_count = Post.objects.count()
        form_data = {
            "text": "Текст изменённого поста",
        }
        response = self.authorized_client.post(
            reverse("posts:post_edit", kwargs={"post_id": self.test_post.id}),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse(
                "posts:post_detail",
                kwargs={"post_id": self.test_post.id}
            ),
        )
        edited_post = Post.objects.get(id=self.test_post.id)
        self.assertEqual(edited_post.text, form_data["text"])
        self.assertEqual(edited_post.group, None)
        self.assertEqual(Post.objects.count(), posts_count)

    def test_create_post_with_image(self):
        """
        Валидная форма с картинкой создает новый Post
        """
        posts_count = Post.objects.count()
        small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x02\x00"
            b"\x01\x00\x80\x00\x00\x00\x00\x00"
            b"\xFF\xFF\xFF\x21\xF9\x04\x00\x00"
            b"\x00\x00\x00\x2C\x00\x00\x00\x00"
            b"\x02\x00\x01\x00\x00\x02\x02\x0C"
            b"\x0A\x00\x3B"
        )
        uploaded = SimpleUploadedFile(
            name="small.gif", content=small_gif, content_type="image/gif"
        )
        form_data = {
            "text": "Пост с картинкой",
            "group": self.group.id,
            "image": uploaded,
        }
        response = self.authorized_client.post(
            reverse("posts:post_create"), data=form_data, follow=True
        )
        self.assertRedirects(
            response,
            reverse(
                "posts:profile",
                kwargs={"username": self.test_author.username}
            ),
        )
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), posts_count + 1)
        # Проверяем наличие поста в базе
        self.assertTrue(
            Post.objects.filter(
                text=form_data["text"],
                group=form_data["group"],
                image="posts/small.gif",
            ).exists()
        )
        # Проверяем, что последний созданный пост - ожидаемый пост
        new_post = Post.objects.all()[0]
        self.assertEqual(new_post.text, form_data["text"])
        self.assertEqual(new_post.group.id, form_data["group"])
        self.assertEqual(new_post.image, "posts/small.gif")
        self.assertEqual(new_post.author, self.test_author)

    def test_create_comment(self):
        """Валидная форма создает новый Comment"""
        comments_count = Comment.objects.count()
        response = self.authorized_client.post(
            reverse(
                "posts:add_comment",
                kwargs={"post_id": self.test_post.id}
            ),
            {"text": "Тестовый коммент!"},
            follow=True,
        )
        self.assertEqual(
            Comment.objects.count(),
            comments_count + 1,
            "Колличество комментариев не увеличилось!"
        )
        last_comment = Comment.objects.latest("id")
        self.assertEqual(
            last_comment.text,
            "Тестовый коммент!",
            "Текст комментария не совпадает с ожидаемым"
        )
        self.assertEqual(
            last_comment.post.id,
            self.test_post.id,
            "Комментарий не привязан к нужному посту"
        )
        self.assertEqual(
            last_comment.author,
            self.test_author,
            "Автор комментария не совпадает с ожидаемым"
        )
        response = self.guest_client.post(
            reverse(
                "posts:add_comment",
                kwargs={"post_id": self.test_post.id}
            ),
            {"text": "Комментарий от неавторизованного пользователя"},
            follow=True,
        )
        comment_reverse = reverse(
            "posts:add_comment",
            kwargs={"post_id": self.test_post.id}
        )
        self.assertRedirects(
            response,
            f"/auth/login/?next={comment_reverse}",
            msg_prefix="Неавторизованного пользователя при "
                       "комментировании не редиректит на страницу логина"
        )
