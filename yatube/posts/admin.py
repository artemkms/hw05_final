from django.contrib import admin

from .models import Comment, Follow, Group, Post


class PostAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "text",
        "pub_date",
        "author",
        "group",
    )
    search_fields = ("text",)
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"
    list_editable = ("group",)


class GroupAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "description",
    )
    search_fields = ("title",)
    list_filter = ("title",)
    empty_value_display = "-пусто-"


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "author",
        "text",
        "created",
        "post",
    )
    search_fields = ("text",)
    empty_value_display = "-пусто-"


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "author",
    )
    search_fields = ("author",)
    empty_value_display = "-пусто-"


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
