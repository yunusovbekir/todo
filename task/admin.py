from django.contrib import admin
from .models import (
    Task,
    Comment,
    Permitted_User,
)


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "author",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("username", "task", "comment_date",)


admin.site.register(Permitted_User)
admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)
