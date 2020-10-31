import subprocess
from django.conf import settings
from django.core.management import BaseCommand
from django.utils.translation import gettext_lazy as _

BASE_DIR = settings.BASE_DIR


class Command(BaseCommand):

    help = _('"Upgrade all pip packages"')
    file = "{}/requirements.txt".format(BASE_DIR)

    def handle(self, *args, **options):
        with open(self.file) as f:

            for line in f.readlines():

                package = self.remove_version(line)

                subprocess.run(
                    'pip install {package} --upgrade'.format(package=package),
                    shell=True
                )

    def remove_version(self, line):
        """
        Remove version from the package title
        input: Django==2.2.0
        output: Django

        """
        package = ''

        for char in line:
            if char != '=':
                package += char
            else:
                break

        return package
