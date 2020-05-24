from django.contrib import admin
from .models import (
    Menu,
    Contact,
    Social_Accounts,
    Website_Settings,
    Contact_Message,
    Portfolio,
)


class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'ordering', 'status', 'url',)


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


admin.site.register(Contact)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Website_Settings, WebsiteSettingsAdmin)
admin.site.register(Contact_Message, ContactMessageAdmin)
admin.site.register(Portfolio, PortfolioAdmin)
