import random
from django.core.management.base import BaseCommand

from records.models import Contact, Dog, Charter, AdoptionStatus, Adoptee
from records.management.helpers.command_helpers import create_contacts_or_adoptees_for_charter

class Command(BaseCommand):
    help = 'Generates realistic test contacts and adoptees per charter for the application.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--countmaxcontact',
            type=int,
            default=150,
            help='max number of contacts to generate (default: 150)'
        )
        parser.add_argument(
            '--countmincontact',
            type=int,
            default=20,
            help='min number of contacts to generate (default: 20)'
        )
        parser.add_argument(
            '--countmaxadoptees',
            type=int,
            default=40,
            help='max number of adoptees to generate (default: 40)'
        )
        parser.add_argument(
            '--countminadoptees',
            type=int,
            default=10,
            help='min number of adoptees to generate (default: 10)'
        )

    def handle(self, *args, **options):
        count_min_contact = options['countmincontact']
        count_max_contact = options['countmaxcontact']
        count_min_adoptees = options['countminadoptees']
        count_max_adoptees = options['countmaxadoptees']

        self.stdout.write(f"Generating {count_min_contact}-{count_max_contact} test contacts per charter...")
        self.stdout.write(f"Generating {count_min_adoptees}-{count_max_adoptees} test adoptees per charter...")

        charters = Charter.objects.all()
        if not charters.exists():
            self.stdout.write(self.style.ERROR("No charters found. Please create a charter first."))
            return
        
        total_contacts_created = 0
        total_adoptees_created = 0
        
        for i, charter in enumerate(charters):
            number_of_contacts = random.randint(count_min_contact, count_max_contact)
            number_of_adoptees = random.randint(count_min_adoptees, count_max_adoptees)
            contacts_created = create_contacts_or_adoptees_for_charter(charter, number_of_contacts, create_adoptees=False)
            adoptees_created = create_contacts_or_adoptees_for_charter(charter, number_of_adoptees, create_adoptees=True)
            total_contacts_created += contacts_created
            total_adoptees_created += adoptees_created

        self.stdout.write(self.style.SUCCESS(f"Successfully created {total_contacts_created} test contacts!"))
        self.stdout.write(self.style.SUCCESS(f"Successfully created {total_adoptees_created} test adoptees!"))
    
        for charter in charters:
            charter_contacts = Contact.objects.filter(adoptee__charter=charter).count()
            charter_adoptees = Adoptee.objects.filter(charter=charter).count()
            self.stdout.write(f"  - {charter.entity_info.name}: {charter_contacts} contacts")
            self.stdout.write(f"  - {charter.entity_info.name}: {charter_adoptees} adoptees")

        self.stdout.write(self.style.SUCCESS("Test contact & adoptee generation complete."))
