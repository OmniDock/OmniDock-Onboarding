from django.core.management.base import BaseCommand
from otto.tasks import OrderTask

class Command(BaseCommand):
    help = 'Fetch data from OTTO API'

    def handle(self, *args, **kwargs):
        OrderTask.run()
        self.stdout.write(self.style.SUCCESS('Successfully fetched and saved OTTO data'))
