from django.contrib import admin
from .models import (
    Task,
    Comment,
    Permitted_User,
    Menu,
    Contact,
    Social_Accounts,
    Website_Settings,
    Contact_Message)


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "author",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("username", "task", "comment_date")


class MenuAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'position', 'ordering',)


class SocialAccountStackInline(admin.StackedInline):
    model = Social_Accounts
    extra = 1


class WebsiteSettingsAdmin(admin.ModelAdmin):
    model = Website_Settings
    list_display = ('__str__',)
    inlines = (
        SocialAccountStackInline,
    )


class ContactMessageAdmin(admin.ModelAdmin):
    model = Contact_Message
    list_display = ('name', 'email', 'subject',)


admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Permitted_User)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Contact)
admin.site.register(Website_Settings, WebsiteSettingsAdmin)
admin.site.register(Contact_Message, ContactMessageAdmin)
