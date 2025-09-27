from django.core.management.base import BaseCommand
from records.models import Charter
from records.models import DogHealthStatus, DogIntakeStatus, DogVaccinationStatus
from records.management.helpers.command_helpers import create_dogs


class Command(BaseCommand):
    help = 'Generate realistic test dogs for development and testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count_max',
            type=int,
            default=100,
            help='Number of dogs to generate (default: 100)'
        )
        parser.add_argument(
            '--count_min',
            type=int,
            default=50,
            help='Number of dogs to generate (default: 50)'
        )
        parser.add_argument(
            '--charter_ids',
            type=int,
            nargs='*',
            default=None,
            help='One or more charter IDs to assign dogs to (optional, space separated)'
        )
        parser.add_argument(
            '--create_owners',
            type=bool,
            default=True,
            help='Create owners for dogs (default: True)'
        )

    def handle(self, *args, **options):
        count_max = options['count_max']
        count_min = options['count_min']
        charter_ids = options.get('charter_ids')
        create_owners = options.get('create_owners')
        
        if charter_ids:
            try:
                charters = [Charter.objects.get(id=charter_id) for charter_id in charter_ids]
            except Charter.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Invalid charter IDs')
                )
                return
        else:
            charters = Charter.objects.all()
            if not charters.exists():
                self.stdout.write(
                    self.style.ERROR('No charters found. Please create a charter first.')
                )
                return


        for charter in charters:
            self.stdout.write(f'Generating {count_min}-{count_max} test dogs for {charter.entity_info.name}...')
            dogs = create_dogs(count_min, count_max, [charter], create_owners=create_owners)
            stats = {
                'health': {
                    'healthy': sum(1 for dog in dogs if dog.health_status == DogHealthStatus.HEALTHY),
                    'sick': sum(1 for dog in dogs if dog.health_status == DogHealthStatus.SICK),
                    'passed': sum(1 for dog in dogs if dog.health_status == DogHealthStatus.PASSED_AWAY),
                    'unspecified': sum(1 for dog in dogs if dog.health_status == DogHealthStatus.UNSPECIFIED),
                },
                'intake': {
                    'rescue': sum(1 for dog in dogs if dog.intake_status == DogIntakeStatus.RESCUE),
                    'training': sum(1 for dog in dogs if dog.intake_status == DogIntakeStatus.TRAINING),
                    'hotel': sum(1 for dog in dogs if dog.intake_status == DogIntakeStatus.HOTEL),
                },
                'vaccination': {
                    'not_vaccinated': sum(1 for dog in dogs if dog.vaccination_status == DogVaccinationStatus.NOT_VACCINATED),
                    'incomplete': sum(1 for dog in dogs if dog.vaccination_status == DogVaccinationStatus.INCOMPLETE),
                    'complete': sum(1 for dog in dogs if dog.vaccination_status == DogVaccinationStatus.COMPLETE),
                    'unspecified': sum(1 for dog in dogs if dog.vaccination_status == DogVaccinationStatus.UNSPECIFIED),
                },
                'owners': {
                    'owner': sum(1 for dog in dogs if dog.owner is not None),
                    'no_owner': sum(1 for dog in dogs if dog.owner is None),
                }
            }


            total_created = sum(stats['health'].values())
            self.stdout.write(f'Successfully created {total_created} test dogs!')
            self.stdout.write('Statistics:')
            self.stdout.write(f'  - Charter: {charter.entity_info.name}')
            self.stdout.write(f'  - Health:')
            self.stdout.write(f'      - Healthy: {stats["health"]["healthy"]}')
            self.stdout.write(f'      - Sick: {stats["health"]["sick"]}')
            self.stdout.write(f'      - Passed Away: {stats["health"]["passed"]}')
            self.stdout.write(f'      - Unspecified: {stats["health"]["unspecified"]}')
            self.stdout.write(f'  - Intake:')
            self.stdout.write(f'      - Rescue: {stats["intake"]["rescue"]}')
            self.stdout.write(f'      - Training: {stats["intake"]["training"]}')
            self.stdout.write(f'      - Hotel: {stats["intake"]["hotel"]}')
            self.stdout.write(f'  - Vaccination:')
            self.stdout.write(f'      - Not Vaccinated: {stats["vaccination"]["not_vaccinated"]}')
            self.stdout.write(f'      - Incomplete: {stats["vaccination"]["incomplete"]}')
            self.stdout.write(f'      - Complete: {stats["vaccination"]["complete"]}')
            self.stdout.write(f'      - Unspecified: {stats["vaccination"]["unspecified"]}')
            self.stdout.write(f'  - Owners:')
            self.stdout.write(f'      - With Owner: {stats["owners"]["owner"]}')
            self.stdout.write(f'      - No Owner: {stats["owners"]["no_owner"]}')

        self.stdout.write(
            self.style.SUCCESS(
                'Test dog data generation complete! '
            )
        )
