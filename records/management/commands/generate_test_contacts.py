import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from records.models import Contact, Dog, Charter, TripleChoice

class Command(BaseCommand):
    help = 'Generates 100 realistic test contacts for the application.'

    def handle(self, *args, **options):
        self.stdout.write("Generating 100 test contacts...")

        # Get existing charters
        charters = Charter.objects.all()
        if not charters.exists():
            self.stdout.write(self.style.ERROR("No charters found. Please create a charter first."))
            return

        # Get existing dogs that are available for adoption
        available_dogs = Dog.objects.filter(is_adopted=False, is_available_for_adoption=True)
        
        # Note: We don't delete existing contacts because some may be referenced by dogs
        # This command will add more contacts to existing ones

        # Common first and last names for realistic data
        first_names = [
            "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
            "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
            "Thomas", "Sarah", "Christopher", "Karen", "Charles", "Nancy", "Daniel", "Lisa",
            "Matthew", "Betty", "Anthony", "Helen", "Mark", "Sandra", "Donald", "Donna",
            "Steven", "Carol", "Paul", "Ruth", "Andrew", "Sharon", "Joshua", "Michelle",
            "Kenneth", "Laura", "Kevin", "Sarah", "Brian", "Kimberly", "George", "Deborah",
            "Timothy", "Dorothy", "Ronald", "Lisa", "Jason", "Nancy", "Edward", "Karen",
            "Jeffrey", "Betty", "Ryan", "Helen", "Jacob", "Sandra", "Gary", "Donna",
            "Nicholas", "Carol", "Eric", "Ruth", "Jonathan", "Sharon", "Stephen", "Michelle",
            "Larry", "Laura", "Justin", "Sarah", "Scott", "Kimberly", "Brandon", "Deborah",
            "Benjamin", "Dorothy", "Samuel", "Amy", "Gregory", "Angela", "Alexander", "Ashley"
        ]

        last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
            "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
            "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
            "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young",
            "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
            "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
            "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker",
            "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy",
            "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson", "Bailey",
            "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson"
        ]

        # Generate realistic contact data
        created_contacts = []
        adopted_dogs = []

        # Sample notes for contacts
        contact_notes = [
            "Interested in adopting a medium-sized dog.",
            "Looking for a family-friendly pet.",
            "Has experience with rescue dogs.",
            "Prefers older, calmer dogs.",
            "Active family, wants an energetic dog.",
            "First-time dog owner, needs guidance.",
            "Has other pets, needs dog-friendly companion.",
            "Looking for a therapy dog candidate.",
            "Interested in fostering before adopting.",
            "Prefers dogs that are good with children.",
            "Has a large yard, perfect for active dogs.",
            "Looking for a senior dog to care for.",
            "Interested in training and rehabilitation.",
            "Wants a dog for emotional support.",
            "Has experience with specific breeds.",
            "Looking for a working dog.",
            "Interested in multiple dogs.",
            "Prefers hypoallergenic breeds.",
            "Has mobility issues, needs calm dog.",
            "Looking for a dog to join their family."
        ]

        for i in range(100):
            # Random charter
            charter = random.choice(charters)
            
            # Generate name
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            name = f"{first_name} {last_name}"
            
            # Generate email
            email = f"{first_name.lower()}.{last_name.lower()}@example.com"
            
            # Generate phone number
            phone = f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            
            # Generate address
            street_number = random.randint(1, 9999)
            street_names = ["Main St", "Oak Ave", "Pine Rd", "Elm St", "Cedar Ln", "Maple Dr", "First St", "Second Ave"]
            street_name = random.choice(street_names)
            cities = ["Anytown", "Springfield", "Riverside", "Oakville", "Greenfield", "Sunset", "Meadowbrook", "Hillcrest"]
            city = random.choice(cities)
            states = ["CA", "NY", "TX", "FL", "IL", "PA", "OH", "GA", "NC", "MI"]
            state = random.choice(states)
            zip_code = f"{random.randint(10000, 99999)}"
            address = f"{street_number} {street_name}, {city}, {state} {zip_code}"
            
            # Generate notes (some contacts have notes, some don't)
            notes = random.choice(contact_notes) if random.random() < 0.7 else ""
            
            # Create the contact
            contact = Contact(
                charter=charter,
                name=name,
                email=email,
                phone=phone,
                address=address,
                notes=notes,
                created=timezone.now(),
                modified=timezone.now()
            )
            contact.save()
            created_contacts.append(contact)

            # Progress indicator
            if (i + 1) % 10 == 0:
                self.stdout.write(f"Created {i + 1}/100 contacts...")

        self.stdout.write(self.style.SUCCESS(f"Successfully created {len(created_contacts)} test contacts!"))

        # Now assign some contacts as dog owners (adopt some dogs)
        if available_dogs.exists():
            self.stdout.write("\nAssigning some contacts as dog owners...")
            
            # Randomly select 20-40% of contacts to become dog owners
            num_adopters = random.randint(20, 40)
            adopters = random.sample(created_contacts, min(num_adopters, len(created_contacts)))
            
            # Get available dogs for adoption
            dogs_to_adopt = list(available_dogs)
            random.shuffle(dogs_to_adopt)
            
            adoption_count = 0
            for adopter in adopters:
                if dogs_to_adopt:
                    dog = dogs_to_adopt.pop()
                    
                    # Update the dog to be adopted
                    dog.owner = adopter
                    dog.is_adopted = True
                    dog.is_available_for_adoption = False
                    dog.adoption_date = timezone.now() - timezone.timedelta(days=random.randint(1, 365))  # Adopted 1 day to 1 year ago
                    dog.save()
                    
                    adopted_dogs.append(dog)
                    adoption_count += 1
                    
                    self.stdout.write(f"  {adopter.name} adopted {dog.name}")

            self.stdout.write(self.style.SUCCESS(f"Successfully assigned {adoption_count} contacts as dog owners!"))

        # Calculate and display statistics
        total_contacts = len(created_contacts)
        dog_owners = len([c for c in created_contacts if c.adopted_dogs.exists()])
        potential_adopters = total_contacts - dog_owners

        self.stdout.write("\nContact Statistics:")
        self.stdout.write(f"  - Total contacts: {total_contacts}")
        self.stdout.write(f"  - Dog owners: {dog_owners}")
        self.stdout.write(f"  - Potential adopters: {potential_adopters}")
        
        if adopted_dogs:
            self.stdout.write(f"  - Dogs adopted: {len(adopted_dogs)}")
        
        # Show contacts by charter
        for charter in charters:
            charter_contacts = Contact.objects.filter(charter=charter).count()
            self.stdout.write(f"  - {charter.name}: {charter_contacts} contacts")

        self.stdout.write(self.style.SUCCESS("Test contact generation complete! You now have realistic contact data for testing."))
