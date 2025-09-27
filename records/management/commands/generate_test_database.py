import random
from django.core.management.base import BaseCommand
from records.models import Charter, EntityInfo, Contact, Dog, DogIntakeStatus, DogHealthStatus, DogVaccinationStatus
from django.db import transaction
from records.management.helpers.command_helpers import create_contacts, create_dogs, create_charters


class Command(BaseCommand):
    help = 'Generates a complete test database with charters, contacts, dogs, and adoption processes.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--charters',
            type=int,
            default=4,
            help='Number of charters to create (default: 4)'
        )
        parser.add_argument(
            '--contacts-min',
            type=int,
            default=200,
            help='Minimum number of contacts to create per charter (default: 200)'
        )
        parser.add_argument(
            '--contacts-max',
            type=int,
            default=400,
            help='Maximum number of contacts to create per charter (default: 400)'
        )
        parser.add_argument(
            '--dogs-min',
            type=int,
            default=50,
            help='Minimum number of dogs per charter (default: 50)'
        )
        parser.add_argument(
            '--dogs-max',
            type=int,
            default=150,
            help='Maximum number of dogs per charter (default: 150)'
        )
        parser.add_argument(
            '--clear-database',
            default=True,
            help='Clear existing data before generating new data'
        )


    def handle(self, *args, **options):
        charters_count = options['charters']
        contacts_min = options['contacts_min']
        contacts_max = options['contacts_max']
        dogs_min = options['dogs_min']
        dogs_max = options['dogs_max']
        clear_database = options['clear_database']

        self.stdout.write(self.style.SUCCESS("🐕 Starting test database generation..."))
        self.stdout.write(f"📊 Configuration:")
        self.stdout.write(f"   - Charters: {charters_count}")
        self.stdout.write(f"   - Contacts: {contacts_min}-{contacts_max}")
        self.stdout.write(f"   - Dogs per charter: {dogs_min}-{dogs_max}")
        self.stdout.write(f"   - Clear existing data: {clear_database}")

        if clear_database:
            self.clear_existing_data()

        self.stdout.write(self.style.WARNING("\n🏢 Step 1: Creating charters..."))
        charters = create_charters(charters_count)

        self.stdout.write(self.style.WARNING("\n🏢 Step 2: Creating contacts..."))
        contacts = create_contacts(contacts_min, contacts_max)

        self.stdout.write(self.style.WARNING("\n🐕 Step 3: Creating dogs..."))
        dogs = create_dogs(dogs_min, dogs_max, charters)

        self.stdout.write(self.style.WARNING("\n📈 Step 4: Generating summary statistics..."))
        self.display_summary_statistics()
        self.stdout.write(self.style.SUCCESS("\n🎉 Test database generation completed successfully!"))

    def clear_existing_data(self):
        """Clear existing data from the database."""
        self.stdout.write("🗑️  Clearing existing data...")
        
        with transaction.atomic():
            Dog.objects.all().delete()
            Contact.objects.all().delete()
            Charter.objects.all().delete()
            EntityInfo.objects.all().delete()
        
        self.stdout.write("✅ Existing data cleared.")


    def display_summary_statistics(self):
        """Display comprehensive statistics about the generated data."""
        total_charters = Charter.objects.count()
        total_contacts = Contact.objects.count()
        total_dogs = Dog.objects.count()

        owned_dogs = Dog.objects.filter(owner__isnull=False).count()
        
        intake_training_dogs = Dog.objects.filter(intake_status=DogIntakeStatus.TRAINING).count()
        intake_hotel_dogs = Dog.objects.filter(intake_status=DogIntakeStatus.HOTEL).count()
        intake_rescue_dogs = Dog.objects.filter(intake_status=DogIntakeStatus.RESCUE).count()

        vaccination_not_vaccinated_dogs = Dog.objects.filter(vaccination_status=DogVaccinationStatus.NOT_VACCINATED).count()
        vaccination_incomplete_dogs = Dog.objects.filter(vaccination_status=DogVaccinationStatus.INCOMPLETE).count()
        vaccination_complete_dogs = Dog.objects.filter(vaccination_status=DogVaccinationStatus.COMPLETE).count()
        vaccination_unspecified_dogs = Dog.objects.filter(vaccination_status=DogVaccinationStatus.UNSPECIFIED).count()        
        
        healthy_dogs = Dog.objects.filter(health_status=DogHealthStatus.HEALTHY).count()
        sick_dogs = Dog.objects.filter(health_status=DogHealthStatus.SICK).count()
        passed_away_dogs = Dog.objects.filter(health_status=DogHealthStatus.PASSED_AWAY).count()
        unspecified_dogs = Dog.objects.filter(health_status=DogHealthStatus.UNSPECIFIED).count()

        self.stdout.write("\n📊 Summary Statistics:")
        self.stdout.write(f"  - Charters: {total_charters}")
        self.stdout.write(f"  - Contacts: {total_contacts}")
        self.stdout.write(f"  - Dogs: {total_dogs}")
        self.stdout.write(f"  - Owned Dogs: {owned_dogs}")
        self.stdout.write(f"  - Intake Reasons:")
        self.stdout.write(f"      - Rescue: {intake_rescue_dogs}")
        self.stdout.write(f"      - Training: {intake_training_dogs}")
        self.stdout.write(f"      - Hotel: {intake_hotel_dogs}")
        self.stdout.write(f"  - Vaccination Status:")
        self.stdout.write(f"      - Not Vaccinated: {vaccination_not_vaccinated_dogs}")
        self.stdout.write(f"      - Incomplete: {vaccination_incomplete_dogs}")
        self.stdout.write(f"      - Complete: {vaccination_complete_dogs}")
        self.stdout.write(f"      - Unspecified: {vaccination_unspecified_dogs}")
        self.stdout.write(f"  - Health Status:")
        self.stdout.write(f"      - Healthy: {healthy_dogs}")
        self.stdout.write(f"      - Sick: {sick_dogs}")
        self.stdout.write(f"      - Passed Away: {passed_away_dogs}")
        self.stdout.write(f"      - Unspecified: {unspecified_dogs}")
        
        

        
