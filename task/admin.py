from django.contrib import admin
from .models import Task, Comment, Permitted_Users


class taskAdmin(admin.ModelAdmin):
    list_display = ("title", "author",)


class permitted_usersAdmin(admin.ModelAdmin):
    list_display = ("task", "permitted_username", "can_comment",)


class commentAdmin(admin.ModelAdmin):
    list_display = ("username", "task", "comment_date")


admin.site.register(Task, taskAdmin)
admin.site.register(Comment, commentAdmin)
admin.site.register(Permitted_Users, permitted_usersAdmin)
