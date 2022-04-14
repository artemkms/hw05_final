from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import CASCADE

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        "Текст поста",
        help_text="Введите текст поста"
    )
    pub_date = models.DateTimeField(
        "Дата публикации",
        auto_now_add=True,
        db_index=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор"
    )

    group = models.ForeignKey(
        Group,
        related_name="posts",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Группа",
        help_text="Выберите группу",
    )
    image = models.ImageField("Картинка", upload_to="posts/", blank=True)

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ("-pub_date",)


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    author = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name="comments"
    )
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ("-created",)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name="follower"
    )
    author = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name="following"
    )

    def __str__(self):
        return self.text

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("user", "author"),
                name="unique_pair"
            ),
        ]
