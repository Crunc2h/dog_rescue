from django.core.management.base import BaseCommand
from records.models import Charter

from records.management.helpers.command_helpers import create_dogs


class Command(BaseCommand):
    help = 'Generate realistic test dogs for development and testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--countmax',
            type=int,
            default=100,
            help='Number of dogs to generate (default: 100)'
        )
        parser.add_argument(
            '--countmin',
            type=int,
            default=50,
            help='Number of dogs to generate (default: 50)'
        )
        parser.add_argument(
            '--charter_id',
            type=int,
            default=None,
            help='Specific charter ID to assign dogs to (optional)'
        )

    def handle(self, *args, **options):
        count_max = options['countmax']
        count_min = options['countmin']
        charter_id = options.get('charter_id')
        
        charters = []
        if not charter_id:
            charters = Charter.objects.all()
            if not charters.exists():
                self.stdout.write(self.style.ERROR("No charters found. Please create a charter first."))
                return
        else:
            try:
                charters.append(Charter.objects.get(id=charter_id))
            except Charter.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Charter with ID {charter_id} not found')
                )
                return

        for charter in charters:
            self.stdout.write(f'Generating {count_min}-{count_max} test dogs...')
            healthy, sick, passed, unspecified = create_dogs(count_min, count_max, charter)

            if healthy == 0 and sick == 0 and passed == 0 and unspecified == 0:
                self.stdout.write(self.style.ERROR("No dogs created. Something went wrong."))
                return

            self.stdout.write(f'Successfully created {healthy + sick + passed + unspecified} test dogs!')
            self.stdout.write(f'Statistics:')
            self.stdout.write(f'  - Charter: {charter.entity_info.name}')
            self.stdout.write(f'  - Healthy: {healthy}')
            self.stdout.write(f'  - Sick: {sick}')
            self.stdout.write(f'  - Passed Away: {passed}')
            self.stdout.write(f'  - Unspecified: {unspecified}')

        self.stdout.write(
            self.style.SUCCESS(
                'Test dog data generation complete! '
            )
        )
