from modeltranslation.translator import translator, TranslationOptions
from .models import Portfolio, Menu, Contact, Website_Settings


class PortfolioTranslation(TranslationOptions):
    fields = (
        'title',
        'description',
    )


class MenuTranslation(TranslationOptions):
    fields = ('title',)


class ContactTranslation(TranslationOptions):
    fields = ('content',)


class WebsiteSettingsTranslation(TranslationOptions):
    fields = (
        'about_app_content',
        'about_me_content',
        'full_name',
    )


translator.register(Portfolio, PortfolioTranslation)
translator.register(Menu, MenuTranslation)
translator.register(Contact, ContactTranslation)
translator.register(Website_Settings, WebsiteSettingsTranslation)
