import random
from django.core.management.base import BaseCommand
from records.management.helpers.command_helpers import create_contacts

class Command(BaseCommand):
    help = 'Generates realistic contacts'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count_max',
            type=int,
            default=150,
            help='max number of contacts to generate (default: 150)'
        )
        parser.add_argument(
            '--count_min',
            type=int,
            default=20,
            help='min number of contacts to generate (default: 20)'
        )


    def handle(self, *args, **options):
        count_min_contact = options['count_min']
        count_max_contact = options['count_max']

        self.stdout.write(f"Generating {count_min_contact}-{count_max_contact} test contacts.")
        
        created_contacts = create_contacts(count_min_contact, count_max_contact)

        self.stdout.write(self.style.SUCCESS(f"Successfully created {len(created_contacts)} test contacts!"))
        self.stdout.write(self.style.SUCCESS("Test contact generation complete."))