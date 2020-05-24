from django.conf import settings


class DbRouter:
    """ A router to control all database operations """

    def db_for_read(self, model, **hints):
        if model._meta.app_label in settings.DATABASE_APPS_MAPPING:
            return settings.DATABASE_APPS_MAPPING.get(model._meta.app_label)
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in settings.DATABASE_APPS_MAPPING:
            return settings.DATABASE_APPS_MAPPING.get(model._meta.app_label)
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'db_mysql' and app_label == 'core':
            return True
        elif app_label and db == 'db_default' and app_label != 'core':
            return True
        return None
