from django.contrib import admin
from .models import (
    Task,
    Comment,
    Permitted_User,
    Menu,
    Contact,
    SocialAccounts,
    WebsiteSettings,
)


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "author",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("username", "task", "comment_date")


class MenuAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'position', 'ordering',)


class SocialAccountStackInline(admin.StackedInline):
    model = SocialAccounts
    extra = 1


class WebsiteSettingsAdmin(admin.ModelAdmin):
    model = WebsiteSettings
    list_display = ('__str__',)
    inlines = (
        SocialAccountStackInline,
    )


admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Permitted_User)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Contact)
admin.site.register(WebsiteSettings, WebsiteSettingsAdmin)
