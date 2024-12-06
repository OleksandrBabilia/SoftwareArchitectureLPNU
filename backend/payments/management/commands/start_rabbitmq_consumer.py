from django.core.management.base import BaseCommand
from payments.consumer import start_consuming

class Command(BaseCommand):
    help = 'Starts the RabbitMQ consumer to listen for payment messages'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting RabbitMQ consumer...')
        start_consuming()
