import random
from django.utils import timezone
from records.models import EntityInfo, Contact, Adoptee, Dog, DogAdoptionRecord, Charter
from records.models import (
    DogGender, DogBreed, DogIntakeReasons, DogColor, 
    DogHealthStatus, DogVaccinationStatus, TripleChoice, AdoptionStatus
)

ADOPTION_NOTES = [
        "Initial meeting went very well. Family seems perfect for this dog.",
        "Home visit completed successfully. Environment is suitable.",
        "Dog showed immediate connection with the family.",
        "Family has experience with rescue dogs and understands needs.",
        "All family members present and engaged during meeting.",
        "Dog was calm and comfortable in the home environment.",
        "Family has other pets that got along well with the dog.",
        "Children were gentle and respectful with the dog.",
        "Family has a large yard perfect for an active dog.",
        "Previous dog experience makes them ideal candidates.",
        "Dog seemed to bond quickly with the primary caregiver.",
        "Family understands the commitment and responsibilities.",
        "Home environment is quiet and stable, good for anxious dogs.",
        "Family has flexible schedule for training and care.",
        "Dog showed signs of being comfortable and relaxed.",
        "Family has researched the breed and understands characteristics.",
        "All necessary supplies and preparations are in place.",
        "Dog responded well to family's energy and lifestyle.",
        "Family is committed to ongoing training and socialization.",
        "Perfect match based on dog's personality and family's needs."
    ]

UNSUCCESSFUL_ADOPTION_NOTES = [
        "Dog was too energetic for the family's lifestyle.",
        "Family's other pets did not get along with the dog.",
        "Dog showed signs of anxiety in the home environment.",
        "Family's schedule was not suitable for dog's needs.",
        "Dog was too large for the family's living space.",
        "Family decided they were not ready for the responsibility.",
        "Dog had behavioral issues that family couldn't handle.",
        "Family's children were too young for this particular dog.",
        "Dog required more exercise than family could provide.",
        "Family's landlord did not allow pets.",
        "Dog showed aggression towards family members.",
        "Family's other commitments prevented proper care.",
        "Dog's medical needs were beyond family's capabilities.",
        "Family decided to wait for a different dog.",
        "Dog was not a good match for family's activity level.",
        "Family's home environment was too stressful for the dog.",
        "Dog required more training than family could provide.",
        "Family's work schedule was incompatible with dog's needs.",
        "Dog showed signs of separation anxiety.",
        "Family decided they preferred a different breed."
]

ADOPTION_SUCCESS_RATE = 0.45
ADOPTION_ONGOING_RATE = 0.35
ADOPTION_UNSUCCESSFUL_RATE = 0.2



def create_adoption_processes():
    """Create adoption processes between adoptees and dogs for all charters."""
    from records.models import AdoptionResult, AdoptionStatus
    
    available_dogs = [dog for dog in Dog.objects.all() if dog.adoption_status == AdoptionStatus.FIT]
    available_adoptees = [adoptee for adoptee in Adoptee.objects.all() if adoptee.adoption_status == AdoptionStatus.FIT]

    if not available_dogs or len(available_adoptees) == 0:
        return 0, 0, 0


    adoption_count = min(len(available_dogs), len(available_adoptees))
    
    selected_dogs = random.sample(available_dogs, adoption_count)
    selected_adoptees = random.sample(available_adoptees, adoption_count)
    
    successful_adoptions = 0
    unsuccessful_adoptions = 0
    ongoing_adoptions = 0

    for i in range(adoption_count):
        dog = selected_dogs[i]
        adoptee = selected_adoptees[i]
    
        
        roll = random.random()
        if roll <= ADOPTION_SUCCESS_RATE:
            result = AdoptionResult.APPROVED
            is_active = True  # Set to True initially, let the model handle it
            notes = random.choice(ADOPTION_NOTES)
            successful_adoptions += 1
        elif roll <= ADOPTION_SUCCESS_RATE + ADOPTION_ONGOING_RATE:
            result = AdoptionResult.EVALUATION
            is_active = True
            notes = random.choice(ADOPTION_NOTES)
            ongoing_adoptions += 1
        else:
            result = AdoptionResult.REJECTED
            is_active = True  # Set to True initially, let the model handle it
            notes = random.choice(UNSUCCESSFUL_ADOPTION_NOTES)
            unsuccessful_adoptions += 1
        
        start_date = timezone.now() - timezone.timedelta(days=random.randint(1, 90))
        if result == AdoptionResult.APPROVED:
            end_date = start_date + timezone.timedelta(days=random.randint(1, 30))
        elif result == AdoptionResult.REJECTED:
            end_date = start_date + timezone.timedelta(days=random.randint(1, 16))
        else:
            end_date = None
        
        adoption_record = DogAdoptionRecord(
            adoptee=adoptee,
            dog=dog,
            result=result,
            notes=notes,
            start_date=start_date,
            end_date=end_date,
            is_active=is_active,
            created=timezone.now(),
            modified=timezone.now()
        )
        
        adoption_record.save()
    return successful_adoptions, ongoing_adoptions, unsuccessful_adoptions

FIRST_NAMES = [
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

LAST_NAMES = [
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

CONTACT_AND_ADOPTEE_NOTES = [
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

STREET_NAMES = ["Main St", "Oak Ave", "Pine Rd", "Elm St", "Cedar Ln", "Maple Dr", "First St", "Second Ave"]
CITIES = ["Istanbul", "Ankara", "Antalya", "Izmir", "Adana", "Bandirma", "Maras", "Malatya"]

def create_contacts_or_adoptees_for_charter(charter, count, create_adoptees=False):
    """Create contacts or adoptees for a specific charter."""
    created = []
    
    for i in range(count):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        name = f"{first_name} {last_name}"
        
        email = f"{first_name.lower()}.{last_name.lower()}@example.com"
        phone = f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        street_number = random.randint(1, 9999)
        street_name = random.choice(STREET_NAMES)
        city = random.choice(CITIES)
        zip_code = f"{random.randint(10000, 99999)}"
        address = f"{street_number} {street_name}, {city}, {zip_code}"
        notes = random.choice(CONTACT_AND_ADOPTEE_NOTES) if random.random() < 0.7 else ""
        
        entity_info = EntityInfo.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address
        )

        if create_adoptees:
            contact_or_adoptee_created = Adoptee(
                entity_info=entity_info,
                charter=charter,
                notes=notes,
                created=timezone.now(),
                modified=timezone.now()
            )
        else:
            contact_or_adoptee_created = Contact(
                entity_info=entity_info,
                notes=notes,
                created=timezone.now(),
                modified=timezone.now()
            )
        created.append(contact_or_adoptee_created)
    
    if create_adoptees:
        for adoptee in created:
            adoptee.save()
    else:
        Contact.objects.bulk_create(created)
    return len(created)

def create_dogs(count_min, count_max, charter=None):
    """Create dogs for a specific charter or all charters."""
    

    healthy, sick, passed, unspecified = [], [], [], []
    
    if charter:
        count = random.randint(count_min, count_max)
        for i in range(count):
            dog = get_random_dog(charter)
            if dog.health_status == DogHealthStatus.HEALTHY:
                healthy.append(dog)
            elif dog.health_status == DogHealthStatus.SICK:
                sick.append(dog)
            elif dog.health_status == DogHealthStatus.PASSED_AWAY:
                passed.append(dog)
            elif dog.health_status == DogHealthStatus.UNSPECIFIED:
                unspecified.append(dog)
    else:
        for charter in Charter.objects.all():
            count = random.randint(count_min, count_max)
            for i in range(count):
                dog = get_random_dog(charter)
                if dog.health_status == DogHealthStatus.HEALTHY:
                    healthy.append(dog)
                elif dog.health_status == DogHealthStatus.SICK:
                    sick.append(dog)
                elif dog.health_status == DogHealthStatus.PASSED_AWAY:
                    passed.append(dog)
                elif dog.health_status == DogHealthStatus.UNSPECIFIED:
                    unspecified.append(dog)
    Dog.objects.bulk_create(healthy + sick + passed + unspecified)
    return len(healthy), len(sick), len(passed), len(unspecified)


DOG_DESCRIPTIONS = [
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

DOG_NAMES = [
        'Buddy', 'Max', 'Bella', 'Charlie', 'Luna', 'Cooper', 'Lucy', 'Rocky',
        'Daisy', 'Bear', 'Molly', 'Duke', 'Sadie', 'Tucker', 'Maggie', 'Zeus',
        'Sophie', 'Jack', 'Chloe', 'Toby', 'Lola', 'Bentley', 'Zoe', 'Oliver',
        'Ruby', 'Winston', 'Penny', 'Murphy', 'Gracie', 'Finn', 'Stella', 'Leo',
        'Lily', 'Milo', 'Nala', 'Oscar', 'Rosie', 'Henry', 'Mia', 'Jake',
        'Coco', 'Sam', 'Emma', 'Rex', 'Abby', 'Gus', 'Willow', 'Bruno',
        'Pepper', 'Rocco', 'Hazel', 'Apollo', 'Ivy', 'Thor', 'Piper', 'Cash',
        'Nova', 'King', 'Scout', 'Prince', 'Sage', 'Diesel', 'Maya', 'Bandit'
]

DOG_HEALTH_RECORDS = [
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

DOG_BEHAVIORAL_NOTES = [
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

DOG_SPECIAL_NEEDS = [
        "", "", "", "", "",
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

DOG_HEALTHY_RATE = 0.80
DOG_UNSPECIFIED_RATE = 0.08
DOG_SICK_RATE = 0.08
DOG_PASSED_AWAY_RATE = 0.04

def get_random_dog(charter):
    name = random.choice(DOG_NAMES)
    age_months = random.randint(2, 120)
    gender = random.choice([DogGender.MALE, DogGender.FEMALE, DogGender.UNSPECIFIED])
    breed = random.choice([choice[0] for choice in DogBreed.choices])
    color = random.choice([choice[0] for choice in DogColor.choices])
    
    vaccination_status = random.choice([choice[0] for choice in DogVaccinationStatus.choices])
    castration_status = random.choice([choice[0] for choice in TripleChoice.choices])
    microchip_status = random.choice([choice[0] for choice in TripleChoice.choices])

    if breed == DogBreed.GOLDEN_RETRIEVER:
        weight = random.uniform(25, 35)
        height = random.uniform(55, 61)
    elif breed == DogBreed.GERMAN_SHEPHERD:
        weight = random.uniform(30, 40)
        height = random.uniform(55, 65)
    elif breed == DogBreed.LABRADOR:
        weight = random.uniform(25, 35)
        height = random.uniform(55, 62)
    elif breed == DogBreed.BEAGLE:
        weight = random.uniform(9, 11)
        height = random.uniform(33, 41)
    elif breed == DogBreed.BULLDOG:
        weight = random.uniform(20, 25)
        height = random.uniform(30, 40)
    elif breed == DogBreed.PITBULL:
        weight = random.uniform(15, 30)
        height = random.uniform(43, 53)
    elif breed == DogBreed.HUSKY:
        weight = random.uniform(20, 27)
        height = random.uniform(51, 60)
    elif breed == DogBreed.CHIHUAHUA:
        weight = random.uniform(1, 3)
        height = random.uniform(15, 23)
    elif breed == DogBreed.POMERANIAN:
        weight = random.uniform(1.5, 3.5)
        height = random.uniform(18, 30)
    else: 
        weight = random.uniform(10, 25)
        height = random.uniform(30, 50)
    
    start_time = timezone.now()
    arrival_date = start_time - timezone.timedelta(days=random.randint(1, 365))

    microchip_id = None
    if microchip_status == TripleChoice.YES:
        microchip_id = f"CHIP{random.randint(100000, 999999)}"

    health_roll = random.random()
    if health_roll <= DOG_HEALTHY_RATE:
        health_status = DogHealthStatus.HEALTHY
    elif health_roll <= DOG_HEALTHY_RATE + DOG_UNSPECIFIED_RATE:
        health_status = DogHealthStatus.UNSPECIFIED
    elif health_roll <= DOG_HEALTHY_RATE + DOG_UNSPECIFIED_RATE + DOG_SICK_RATE:
        health_status = DogHealthStatus.SICK
    else:
        health_status = DogHealthStatus.PASSED_AWAY
        
    
    if health_status == DogHealthStatus.HEALTHY:
        adoption_status = AdoptionStatus.FIT
    elif health_status == DogHealthStatus.SICK or health_status == DogHealthStatus.PASSED_AWAY:
        adoption_status = AdoptionStatus.UNFIT
    elif health_status == DogHealthStatus.UNSPECIFIED:
        adoption_status = AdoptionStatus.UNSPECIFIED

    return Dog(
            name=name,
            age_months=age_months,
            gender=gender,
            breed=breed,
            microchip_status=microchip_status,
            microchip_id=microchip_id,
            intake_reason=DogIntakeReasons.RESCUE,
            arrival_date=arrival_date,
            charter=charter,
            adoption_status=adoption_status,
            current_weight_kg=round(weight, 1),
            height_cm=round(height, 1),
            color=color,
            detailed_description=random.choice(DOG_DESCRIPTIONS),
            health_status=health_status,
            vaccination_status=vaccination_status,
            castration_status=castration_status,
            health_record=random.choice(DOG_HEALTH_RECORDS),
            vaccination_record="DHPP, Rabies, Bordetella - all current",
            treatment_record="Regular flea/tick prevention, heartworm prevention",
            special_needs=random.choice(DOG_SPECIAL_NEEDS),
            behavioral_notes=random.choice(DOG_BEHAVIORAL_NOTES),
            other_notes=f"test dog",
            created=timezone.now(),
            modified=timezone.now()
    )


    
CHARTER_NAMES = [
    'TEST KK_ISTANBUL',
    'TEST KK_BANDIRMA',
    'TEST KK_ANKARA',
    'TEST KK_IZMIR',
    'TEST KK_ANTALYA',
    'TEST KK_BURSA',
    'TEST KK_DENIZLI',
    'TEST KK_KONYA',
    'TEST KK_KAYSERI',
    'TEST KK_MALATYA',
    'TEST KK_SAMSUN',
    'TEST KK_SINOP',
    'TEST KK_TEKIRDAG',
]
    
def create_charters(count):
    """Create charters with realistic data."""
    
    charters = []
    for i in range(count):
        name = CHARTER_NAMES[i] if i < len(CHARTER_NAMES) else f"TEST Charter {i+1}"
        
        entity_info = EntityInfo.objects.create(
            name=name,
            email=f"info@{name.lower().replace(' ', '')}.org",
            phone=f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            address=f"{random.randint(100, 9999)} {random.choice(['Main St', 'Oak Ave', 'Pine Rd', 'Elm St'])} {random.choice(['Anytown', 'Springfield', 'Riverside', 'Oakville'])} {random.choice(['CA', 'NY', 'TX', 'FL'])} {random.randint(10000, 99999)}"
        )
        charter =Charter.objects.create(
            entity_info=entity_info
        )
        charters.append(charter)
    return charters