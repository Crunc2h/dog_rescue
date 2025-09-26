from django.core.management.base import BaseCommand
from records.models import Dog, Adoptee, AdoptionStatus
from records.management.helpers.command_helpers import create_adoption_processes


class Command(BaseCommand):
    help = 'Generates realistic adoption processes between adoptees and dogs available for adoption.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Number of adoption processes to generate (default: 50)'
        )
        parser.add_argument(
            '--depth',
            type=int,
            default=3,
            help='How many levels of depth to generate adoption processes for (default: 3)'
        )

    def handle(self, *args, **options):
        count = options['count']
        depth = options['depth']
        if depth <= 0:
            self.stdout.write(self.style.ERROR("Depth must be greater than 0"))
            return
        
        self.stdout.write(f"Generating {count} adoption processes...")
        
        adoptees = list(Adoptee.objects.all())
        if not adoptees:
            self.stdout.write(self.style.ERROR("No adoptee found. Please create adoptees first."))
            return
        
        available_dogs = Dog.objects.filter(adoption_status=AdoptionStatus.FIT)
        if not available_dogs.exists():
            self.stdout.write(self.style.ERROR("No available dogs found. Please create dogs first."))
            return
        
        total_successful, total_ongoing, total_unsuccessful = 0,0,0
        for i in range(depth):
            successful, ongoing, unsuccessful = create_adoption_processes()
            total_successful += successful
            total_ongoing += ongoing
            total_unsuccessful += unsuccessful
        
        self.stdout.write(self.style.SUCCESS(f"Successfully created adoption processes!"))
        self.stdout.write(f"  - Successful: {total_successful}")
        self.stdout.write(f"  - Ongoing: {total_ongoing}")
        self.stdout.write(f"  - Unsuccessful: {total_unsuccessful}")
