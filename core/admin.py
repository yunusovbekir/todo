from django.contrib import admin
from .models import Task, Comment, Permitted_User, Menu


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "author",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("username", "task", "comment_date")


class MenuAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'position', 'ordering',)


admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Permitted_User)
admin.site.register(Menu, MenuAdmin)
