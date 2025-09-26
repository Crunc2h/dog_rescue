import random
from django.core.management.base import BaseCommand
from records.models import Charter, EntityInfo, Contact, Adoptee, Dog, DogAdoptionRecord, AdoptionStatus, DogHealthStatus, AdoptionResult
from django.db import transaction
from records.management.helpers.command_helpers import create_contacts_or_adoptees_for_charter, create_dogs, create_adoption_processes, create_charters


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
            '--adoptees-min',
            type=int,
            default=15,
            help='Minimum number of adoptees per charter (default: 15)'
        )
        parser.add_argument(
            '--adoptees-max',
            type=int,
            default=40,
            help='Maximum number of adoptees per charter (default: 40)'
        )
        parser.add_argument(
            '--clear-database',
            default=True,
            help='Clear existing data before generating new data'
        )
        parser.add_argument(
            '--depth',
            type=int,
            default=3,
            help='How many levels of depth to generate adoption processes for (default: 3)'
        )

    def handle(self, *args, **options):
        charters_count = options['charters']
        contacts_min = options['contacts_min']
        contacts_max = options['contacts_max']
        dogs_min = options['dogs_min']
        dogs_max = options['dogs_max']
        adoptees_min = options['adoptees_min']
        adoptees_max = options['adoptees_max']
        clear_database = options['clear_database']
        depth = options['depth']
        if depth <= 0:
            self.stdout.write(self.style.ERROR("Depth must be greater than 0"))
            return

        self.stdout.write(self.style.SUCCESS("🐕 Starting comprehensive test database generation..."))
        self.stdout.write(f"📊 Configuration:")
        self.stdout.write(f"   - Charters: {charters_count}")
        self.stdout.write(f"   - Contacts: {contacts_min}-{contacts_max}")
        self.stdout.write(f"   - Dogs per charter: {dogs_min}-{dogs_max}")
        self.stdout.write(f"   - Adoptees per charter: {adoptees_min}-{adoptees_max}")
        self.stdout.write(f"   - Clear existing data: {clear_database}")

        if clear_database:
            self.clear_existing_data()

        self.stdout.write(self.style.WARNING("\n🏢 Step 1: Creating charters..."))
        charters = create_charters(charters_count)

        

        self.stdout.write(self.style.WARNING("\n🏢 Step 2: Populating charters..."))
        for i, charter in enumerate(charters):
            self.stdout.write(self.style.WARNING(f"\n👥 Step 2-{i+1}-1: Creating contacts for {charter.entity_info.name}..."))
            total_contacts = random.randint(contacts_min, contacts_max)
            create_contacts_or_adoptees_for_charter(charter, total_contacts, create_adoptees=False)

            self.stdout.write(self.style.WARNING(f"\n👥 Step 2-{i+1}-2: Creating adoptees for {charter.entity_info.name}..."))
            total_adoptees = random.randint(adoptees_min, adoptees_max)
            create_contacts_or_adoptees_for_charter(charter, total_adoptees, create_adoptees=True)
            
            self.stdout.write(self.style.WARNING(f"\n🐕 Step 2-{i+1}-3: Creating dogs for {charter.entity_info.name}..."))
            healthy, sick, passed, unspecified = create_dogs(dogs_min, dogs_max, charter)
            if healthy == 0 and sick == 0 and passed == 0 and unspecified == 0:
                self.stdout.write(self.style.ERROR("No dogs created. Something went wrong."))
                return
            
        self.stdout.write(self.style.WARNING(f"\n💕 Step 3: Generating adoption processes..."))
        total_successful, total_ongoing, total_unsuccessful = 0,0,0
        for i in range(depth):
            self.stdout.write(self.style.WARNING(f"\n💕 Step 3-{i+1}: Creating adoption processes for depth {i+1}..."))
            successful, ongoing, unsuccessful = create_adoption_processes()
            total_successful += successful
            total_ongoing += ongoing
            total_unsuccessful += unsuccessful

        self.stdout.write(self.style.WARNING(f"\n💕 Total successful adoption processes: {total_successful}"))
        self.stdout.write(self.style.WARNING(f"\n💕 Total ongoing adoption processes: {total_ongoing}"))
        self.stdout.write(self.style.WARNING(f"\n💕 Total unsuccessful adoption processes: {total_unsuccessful}"))

        self.stdout.write(self.style.WARNING("\n📈 Step 4: Generating summary statistics..."))
        self.display_summary_statistics()
        self.stdout.write(self.style.SUCCESS("\n🎉 Test database generation completed successfully!"))

    def clear_existing_data(self):
        """Clear existing data from the database."""
        self.stdout.write("🗑️  Clearing existing data...")
        
        with transaction.atomic():
            DogAdoptionRecord.objects.all().delete()
            Dog.objects.all().delete()
            Adoptee.objects.all().delete()
            Contact.objects.all().delete()
            Charter.objects.all().delete()
            EntityInfo.objects.all().delete()
        
        self.stdout.write("✅ Existing data cleared.")


    def display_summary_statistics(self):
        """Display comprehensive statistics about the generated data."""
        total_charters = Charter.objects.count()
        total_contacts = Contact.objects.count()
        total_adoptees = Adoptee.objects.count()
        
        total_dogs = Dog.objects.count()
        total_adoptions = DogAdoptionRecord.objects.count()
        
        owned_dogs = Dog.objects.filter(owner__isnull=False).count()
        adopted_dogs = Dog.objects.filter(adoption_status=AdoptionStatus.ADOPTED).count()
        fit_dogs = Dog.objects.filter(adoption_status=AdoptionStatus.FIT).count()
        unfit_dogs = Dog.objects.filter(adoption_status=AdoptionStatus.UNFIT).count()
        unspecified_dogs = Dog.objects.filter(adoption_status=AdoptionStatus.UNSPECIFIED).count()
        trial_dogs = Dog.objects.filter(adoption_status=AdoptionStatus.TRIAL).count()

        owners_adoptees = Adoptee.objects.filter(adopted_dogs__isnull=False).count()
        trial_adoptees = Adoptee.objects.filter(adoption_status=AdoptionStatus.TRIAL).count()
        fit_adoptees = Adoptee.objects.filter(adoption_status=AdoptionStatus.FIT).count()
        unfit_adoptees = Adoptee.objects.filter(adoption_status=AdoptionStatus.UNFIT).count()
        unspecified_adoptees = Adoptee.objects.filter(adoption_status=AdoptionStatus.UNSPECIFIED).count()
        adoptee_adoptation_status_sanity = (
        Adoptee.objects.filter(adoption_status=AdoptionStatus.ADOPTED).count()
        )
        
        healthy_dogs = Dog.objects.filter(health_status=DogHealthStatus.HEALTHY).count()
        sick_dogs = Dog.objects.filter(health_status=DogHealthStatus.SICK).count()
        passed_away_dogs = Dog.objects.filter(health_status=DogHealthStatus.PASSED_AWAY).count()
        unspecified_dogs = Dog.objects.filter(health_status=DogHealthStatus.UNSPECIFIED).count()
        
        successful_adoptions = DogAdoptionRecord.objects.filter(result=AdoptionResult.APPROVED).count()
        rejected_adoptions = DogAdoptionRecord.objects.filter(result=AdoptionResult.REJECTED).count()
        evaluation_adoptions = DogAdoptionRecord.objects.filter(result=AdoptionResult.EVALUATION).count()
        adoption_records_sanity = (
        DogAdoptionRecord.objects.filter(result=AdoptionResult.APPROVED, is_active=True).count()
        + DogAdoptionRecord.objects.filter(result=AdoptionResult.REJECTED, is_active=True).count()
        + DogAdoptionRecord.objects.filter(result=AdoptionResult.EVALUATION, is_active=False).count()
        )

        self.stdout.write(self.style.SUCCESS("\n📊 DATABASE SUMMARY STATISTICS"))
        self.stdout.write("=" * 50)
        self.stdout.write(f"🏢 Total Charters: {total_charters}")
        self.stdout.write(f"🐕 Total Dogs: {total_dogs}")
        self.stdout.write(f"👥 Total Contacts: {total_contacts}")
        self.stdout.write(f"👥 Total Adoptees: {total_adoptees}")
        self.stdout.write(f"💕 Total Adoption Processes: {total_adoptions}")
        self.stdout.write("")
        self.stdout.write("🐕 DOG STATISTICS - ADOPTION STATUS:")
        self.stdout.write(f"   - Adopted: {adopted_dogs}")
        self.stdout.write(f"   - Owned (!!! SHOULD BE EQUAL TO ADOPTED DOGS !!!): {owned_dogs}")
        self.stdout.write(f"   - Fit (Available for adoption): {fit_dogs}")
        self.stdout.write(f"   - Unfit (Not ready for adoption): {unfit_dogs}")
        self.stdout.write(f"   - Unspecified: {unspecified_dogs}")
        self.stdout.write(f"   - Trial: {trial_dogs}")
        self.stdout.write("")
        self.stdout.write("🐕 DOG STATISTICS - HEALTH STATE:")
        self.stdout.write(f"   - Healthy: {healthy_dogs}")
        self.stdout.write(f"   - Sick: {sick_dogs}")
        self.stdout.write(f"   - Passed Away: {passed_away_dogs}")
        self.stdout.write(f"   - Unspecified: {unspecified_dogs}")
        self.stdout.write("")
        self.stdout.write("💕 ADOPTEE STATISTICS:")
        self.stdout.write(f"   - Owners: {owners_adoptees}")
        self.stdout.write(f"   - Trial: {trial_adoptees}")
        self.stdout.write(f"   - Fit (Available for adoption): {fit_adoptees}")
        self.stdout.write(f"   - Unfit (Not ready for adoption): {unfit_adoptees}")
        self.stdout.write(f"   - Unspecified: {unspecified_adoptees}")
        self.stdout.write(f"   - Adoption Status Sanity Check (!!! SHOULD BE 0 !!!): {adoptee_adoptation_status_sanity}")
        self.stdout.write("")
        self.stdout.write("💕 ADOPTION RECORDS STATISTICS:")
        self.stdout.write(f"   - Successful (!!! SHOULD BE EQUAL TO ADOPTED DOGS !!!): {successful_adoptions}")
        self.stdout.write(f"   - Rejected: {rejected_adoptions}")
        self.stdout.write(f"   - Under Evaluation: {evaluation_adoptions}")
        self.stdout.write(f"   - Adoption Records Sanity Check (!!! SHOULD BE 0 !!!): {adoption_records_sanity}")
