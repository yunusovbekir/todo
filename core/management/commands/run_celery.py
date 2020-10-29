from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        """ custom run celery command """

        import subprocess
        command = "celery --app=app.celery:app worker -B --loglevel=INFO"
        subprocess.run(command, shell=True)
