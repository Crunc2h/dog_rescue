from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
import random
from records.models import Dog, Charter, Contact
from records.models import (
    DogGender, DogBreed, DogIntakeReasons, DogColor, 
    DogHealthStatus, DogVaccinationStatus, TripleChoice
)


class Command(BaseCommand):
    help = 'Generate 100 realistic test dogs for development and testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=100,
            help='Number of dogs to generate (default: 100)'
        )
        parser.add_argument(
            '--charter-id',
            type=int,
            help='Specific charter ID to assign dogs to (optional)'
        )

    def handle(self, *args, **options):
        count = options['count']
        charter_id = options.get('charter_id')
        
        # Get or create a default charter
        if charter_id:
            try:
                charter = Charter.objects.get(id=charter_id)
            except Charter.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Charter with ID {charter_id} not found')
                )
                return
        else:
            charter, created = Charter.objects.get_or_create(
                name="Test Charter Organization",
                defaults={'name': 'Test Charter Organization'}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created new charter: {charter.name}')
                )

        # Realistic dog names
        dog_names = [
            'Buddy', 'Max', 'Bella', 'Charlie', 'Luna', 'Cooper', 'Lucy', 'Rocky',
            'Daisy', 'Bear', 'Molly', 'Duke', 'Sadie', 'Tucker', 'Maggie', 'Zeus',
            'Sophie', 'Jack', 'Chloe', 'Toby', 'Lola', 'Bentley', 'Zoe', 'Oliver',
            'Ruby', 'Winston', 'Penny', 'Murphy', 'Gracie', 'Finn', 'Stella', 'Leo',
            'Lily', 'Milo', 'Nala', 'Oscar', 'Rosie', 'Henry', 'Mia', 'Jake',
            'Coco', 'Sam', 'Emma', 'Rex', 'Abby', 'Gus', 'Willow', 'Bruno',
            'Pepper', 'Rocco', 'Hazel', 'Apollo', 'Ivy', 'Thor', 'Piper', 'Cash',
            'Nova', 'King', 'Scout', 'Prince', 'Sage', 'Diesel', 'Maya', 'Bandit',
            'Luna', 'Shadow', 'Ruby', 'Zeus', 'Stella', 'Apollo', 'Bella', 'Duke',
            'Molly', 'Bear', 'Sophie', 'Rocky', 'Chloe', 'Tucker', 'Lola', 'Jack',
            'Zoe', 'Oliver', 'Penny', 'Murphy', 'Gracie', 'Finn', 'Rosie', 'Henry',
            'Mia', 'Jake', 'Emma', 'Rex', 'Abby', 'Gus', 'Willow', 'Bruno',
            'Pepper', 'Rocco', 'Hazel', 'Piper', 'Cash', 'Nova', 'King', 'Scout'
        ]

        # Realistic descriptions
        descriptions = [
            "Friendly and energetic dog who loves to play fetch and go on walks.",
            "Gentle and calm companion, great with children and other pets.",
            "Active and intelligent dog who enjoys learning new tricks.",
            "Loyal and protective, makes an excellent family pet.",
            "Playful and social dog who loves meeting new people.",
            "Quiet and well-behaved, perfect for apartment living.",
            "Adventurous and curious, always ready for outdoor activities.",
            "Sweet and affectionate, loves cuddles and attention.",
            "Smart and trainable, responds well to positive reinforcement.",
            "Energetic and fun-loving, great for active families.",
            "Calm and patient, excellent with elderly owners.",
            "Confident and outgoing, loves being the center of attention.",
            "Gentle giant with a heart of gold.",
            "Small but mighty, full of personality and charm.",
            "Rescue dog with a grateful and loving spirit.",
            "Well-socialized and comfortable in various environments.",
            "Natural protector with a gentle nature.",
            "Playful puppy energy in an adult dog body.",
            "Loyal companion who will follow you anywhere.",
            "Independent yet loving, perfect for busy lifestyles."
        ]

        # Health records
        health_records = [
            "Regular checkups, all vaccinations up to date. No known health issues.",
            "Recently treated for minor skin irritation, now fully recovered.",
            "Spayed/neutered, all routine care completed. Healthy and active.",
            "Previous owner reported good health, no medical concerns noted.",
            "Rescue dog, undergoing routine health assessment. Appears healthy.",
            "All vaccinations current, dental cleaning completed last month.",
            "No known allergies or health conditions. Regular exercise recommended.",
            "Microchipped and registered. Annual checkup due in 6 months.",
            "Healthy weight maintained through proper diet and exercise.",
            "Recent blood work shows excellent health markers.",
            "Minor dental work completed, now in perfect health.",
            "All routine care up to date, no ongoing health concerns.",
            "Rescue with no known health issues, adapting well to new environment.",
            "Regular grooming and health maintenance, excellent condition.",
            "Previous minor injury fully healed, no lasting effects.",
            "Healthy senior dog with age-appropriate care plan.",
            "All vaccinations and preventatives current, excellent health.",
            "Regular exercise and proper nutrition maintaining optimal health.",
            "No known genetic health issues, well-bred lineage.",
            "Comprehensive health check completed, all systems normal."
        ]

        # Behavioral notes
        behavioral_notes = [
            "Well-mannered and house-trained. Gets along with other dogs.",
            "Loves children and is very gentle with them.",
            "High energy, needs regular exercise and mental stimulation.",
            "Calm and quiet, perfect for apartment living.",
            "Social butterfly, loves meeting new people and dogs.",
            "Independent but affectionate, good for first-time owners.",
            "Protective of family, excellent watchdog qualities.",
            "Playful and goofy, brings joy to everyone around.",
            "Intelligent and eager to please, learns commands quickly.",
            "Loyal companion, forms strong bonds with family members.",
            "Confident and outgoing, great for social situations.",
            "Gentle and patient, excellent with elderly or disabled owners.",
            "Active and adventurous, loves outdoor activities.",
            "Quiet and well-behaved, doesn't bark excessively.",
            "Friendly with strangers, no aggression issues.",
            "Good with cats and other small animals.",
            "Loves car rides and traveling with family.",
            "Enjoys puzzle toys and mental challenges.",
            "Well-socialized from puppyhood, comfortable in crowds.",
            "Rescue dog adjusting well, showing increasing confidence."
        ]

        # Special needs
        special_needs = [
            "",  # Most dogs have no special needs
            "",
            "",
            "",
            "",
            "Requires daily medication for minor condition.",
            "Needs special diet for sensitive stomach.",
            "Requires regular grooming due to coat type.",
            "Needs joint supplements due to age.",
            "Requires quiet environment due to anxiety.",
            "Needs regular exercise to prevent weight gain.",
            "Requires dental care due to previous neglect.",
            "Needs socialization training with other dogs.",
            "Requires leash training for outdoor activities.",
            "Needs crate training for house manners.",
            "Requires patience during adjustment period.",
            "Needs regular nail trimming due to quick growth.",
            "Requires ear cleaning due to breed characteristics.",
            "Needs eye drops for minor condition.",
            "Requires special harness due to neck sensitivity."
        ]

        # Generate dogs
        created_dogs = []
        start_time = timezone.now()
        
        self.stdout.write(f'Generating {count} test dogs...')
        
        for i in range(count):
            # Random data generation
            name = random.choice(dog_names)
            age_months = random.randint(2, 120)  # 2 months to 10 years
            gender = random.choice([DogGender.MALE, DogGender.FEMALE, DogGender.UNSPECIFIED])
            breed = random.choice([choice[0] for choice in DogBreed.choices])
            color = random.choice([choice[0] for choice in DogColor.choices])
            health_status = random.choice([choice[0] for choice in DogHealthStatus.choices])
            vaccination_status = random.choice([choice[0] for choice in DogVaccinationStatus.choices])
            castration_status = random.choice([choice[0] for choice in TripleChoice.choices])
            microchip_status = random.choice([choice[0] for choice in TripleChoice.choices])
            
            # Weight and height based on breed and age
            if breed == DogBreed.GOLDEN_RETRIEVER:
                weight = random.uniform(25, 35)
                height = random.uniform(55, 61)
            elif breed == DogBreed.GERMAN_SHEPHERD:
                weight = random.uniform(30, 40)
                height = random.uniform(55, 65)
            else:  # Street dog or mixed
                weight = random.uniform(10, 25)
                height = random.uniform(30, 50)
            
            # Adoption status (70% available, 30% adopted)
            is_adopted = random.random() < 0.3
            is_available = not is_adopted or random.random() < 0.1  # Some adopted dogs still show as available
            
            # Random dates
            arrival_date = start_time - timedelta(days=random.randint(1, 365))
            adoption_date = None
            if is_adopted:
                adoption_date = arrival_date + timedelta(days=random.randint(1, 200))
            
            # Microchip ID if chipped
            microchip_id = None
            if microchip_status == TripleChoice.YES:
                microchip_id = f"CHIP{random.randint(100000, 999999)}"
            
            # Create the dog
            dog = Dog(
                name=name,
                age_months=age_months,
                gender=gender,
                breed=breed,
                microchip_status=microchip_status,
                microchip_id=microchip_id,
                intake_reason=DogIntakeReasons.RESCUE,
                arrival_date=arrival_date,
                charter=charter,
                is_adopted=is_adopted,
                is_available_for_adoption=is_available,
                adoption_date=adoption_date,
                weight_kg=round(weight, 1),
                height_cm=round(height, 1),
                color=color,
                detailed_description=random.choice(descriptions),
                health_status=health_status,
                vaccination_status=vaccination_status,
                castration_status=castration_status,
                health_record=random.choice(health_records),
                vaccination_record="DHPP, Rabies, Bordetella - all current",
                treatment_record="Regular flea/tick prevention, heartworm prevention",
                special_needs=random.choice(special_needs),
                behavioral_notes=random.choice(behavioral_notes),
                other_notes=f"Generated test dog #{i+1} for development purposes."
            )
            dog.save()
            
            created_dogs.append(dog)
            
            # Progress indicator
            if (i + 1) % 10 == 0:
                self.stdout.write(f'Created {i + 1}/{count} dogs...')

        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(created_dogs)} test dogs!'
            )
        )
        
        # Statistics
        adopted_count = sum(1 for dog in created_dogs if dog.is_adopted)
        available_count = sum(1 for dog in created_dogs if dog.is_available_for_adoption)
        healthy_count = sum(1 for dog in created_dogs if dog.health_status == DogHealthStatus.HEALTHY)
        
        self.stdout.write(f'Statistics:')
        self.stdout.write(f'  - Adopted: {adopted_count}')
        self.stdout.write(f'  - Available: {available_count}')
        self.stdout.write(f'  - Healthy: {healthy_count}')
        self.stdout.write(f'  - Charter: {charter.name}')
        
        self.stdout.write(
            self.style.SUCCESS(
                'Test data generation complete! You can now test your application with realistic data.'
            )
        )
