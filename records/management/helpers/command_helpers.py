import random
from django.utils import timezone
from records.models import EntityInfo, Contact, Dog, Charter
from records.models import (
    DogGender, DogBreed, DogIntakeStatus, DogColor, 
    DogHealthStatus, DogVaccinationStatus, TripleChoice
)



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


def get_random_contact():
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

    return Contact(
        entity_info=entity_info,
        notes=notes
    )


def create_contacts(count_min, count_max):
    """Create random contacts of a given count"""
    contacts = [get_random_contact()for i in range(random.randint(count_min, count_max)) ]
    Contact.objects.bulk_create(contacts)
    return contacts


DOG_HEALTHY_RATE_MIN = 0.75
DOG_HEALTHY_RATE_MAX = 0.90
DOG_SICK_RATE_MIN = 0.05
DOG_SICK_RATE_MAX = 0.15
DOG_PASSED_AWAY_RATE_MIN = 0.05
DOG_PASSED_AWAY_RATE_MAX = 0.08
DOG_UNSPECIFIED_RATE_MIN = 0.03
DOG_UNSPECIFIED_RATE_MAX = 0.05

def get_health_values_for_charter():
    healthy_rate = random.uniform(DOG_HEALTHY_RATE_MIN, DOG_HEALTHY_RATE_MAX)
    unspecified_rate = random.uniform(DOG_UNSPECIFIED_RATE_MIN, DOG_UNSPECIFIED_RATE_MAX)
    sick_rate = random.uniform(DOG_SICK_RATE_MIN, DOG_SICK_RATE_MAX)
    passed_away_rate = random.uniform(DOG_PASSED_AWAY_RATE_MIN, DOG_PASSED_AWAY_RATE_MAX)
    total = healthy_rate + unspecified_rate + sick_rate + passed_away_rate
    scale = 1.0 / total
    healthy_rate *= scale
    unspecified_rate *= scale
    sick_rate *= scale
    passed_away_rate *= scale
    return {
        "healthy_rate": healthy_rate,
        "unspecified_rate": unspecified_rate,
        "sick_rate": sick_rate,
        "passed_away_rate": passed_away_rate
    }

DOG_VACCINATION_COMPLETE_RATE_MIN = 0.40
DOG_VACCINATION_COMPLETE_RATE_MAX = 0.50
DOG_VACCINATION_INCOMPLETE_RATE_MIN = 0.10
DOG_VACCINATION_INCOMPLETE_RATE_MAX = 0.15
DOG_VACCINATION_NOT_VACCINATED_RATE_MIN = 0.05
DOG_VACCINATION_NOT_VACCINATED_RATE_MAX = 0.08
DOG_VACCINATION_UNSPECIFIED_RATE_MIN = 0.03
DOG_VACCINATION_UNSPECIFIED_RATE_MAX = 0.05

def get_vaccination_values_for_charter():
    complete_rate = random.uniform(DOG_VACCINATION_COMPLETE_RATE_MIN, DOG_VACCINATION_COMPLETE_RATE_MAX)
    incomplete_rate = random.uniform(DOG_VACCINATION_INCOMPLETE_RATE_MIN, DOG_VACCINATION_INCOMPLETE_RATE_MAX)
    not_vaccinated_rate = random.uniform(DOG_VACCINATION_NOT_VACCINATED_RATE_MIN, DOG_VACCINATION_NOT_VACCINATED_RATE_MAX)
    unspecified_rate = random.uniform(DOG_VACCINATION_UNSPECIFIED_RATE_MIN, DOG_VACCINATION_UNSPECIFIED_RATE_MAX)
    total = complete_rate + incomplete_rate + not_vaccinated_rate + unspecified_rate
    scale = 1.0 / total
    complete_rate *= scale
    incomplete_rate *= scale
    not_vaccinated_rate *= scale
    unspecified_rate *= scale
    return {
        "complete_rate": complete_rate,
        "incomplete_rate": incomplete_rate,
        "not_vaccinated_rate": not_vaccinated_rate,
        "unspecified_rate": unspecified_rate
    }
    
DOG_INTAKE_RESCUE_RATE_MIN = 0.80
DOG_INTAKE_RESCUE_RATE_MAX = 0.90
DOG_INTAKE_TRAINING_RATE_MIN = 0.10
DOG_INTAKE_TRAINING_RATE_MAX = 0.15
DOG_INTAKE_HOTEL_RATE_MIN = 0.05
DOG_INTAKE_HOTEL_RATE_MAX = 0.08

def get_intake_values_for_charter():
    intake_rate = random.uniform(DOG_INTAKE_RESCUE_RATE_MIN, DOG_INTAKE_RESCUE_RATE_MAX)
    training_rate = random.uniform(DOG_INTAKE_TRAINING_RATE_MIN, DOG_INTAKE_TRAINING_RATE_MAX)
    hotel_rate = random.uniform(DOG_INTAKE_HOTEL_RATE_MIN, DOG_INTAKE_HOTEL_RATE_MAX)
    total = intake_rate + training_rate + hotel_rate
    scale = 1.0 / total
    intake_rate *= scale
    training_rate *= scale
    hotel_rate *= scale
    return {
        "intake_rate": intake_rate,
        "training_rate": training_rate,
        "hotel_rate": hotel_rate
    }

def create_dogs(count_min, count_max, charters, create_owners=True):
    """Create random dogs in given range for given charters."""
    dogs = []
    for charter in charters:
        health_values = get_health_values_for_charter()
        vaccination_values = get_vaccination_values_for_charter()
        intake_values = get_intake_values_for_charter()
        dogs_created = [get_random_dog(health_values, vaccination_values, intake_values, charter, create_owners) for i in range(random.randint(count_min, count_max))]
        dogs.extend(dogs_created)
    Dog.objects.bulk_create(dogs)
    return dogs

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


def get_random_dog(health_values, vaccination_values, intake_values, charter, create_owners=True):
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
    if health_roll <= health_values["healthy_rate"]:
        health_status = DogHealthStatus.HEALTHY
    elif health_roll <= health_values['healthy_rate'] + health_values["unspecified_rate"]:
        health_status = DogHealthStatus.UNSPECIFIED
    elif health_roll <= health_values['healthy_rate'] + health_values["unspecified_rate"] + health_values["sick_rate"]:
        health_status = DogHealthStatus.SICK
    else:
        health_status = DogHealthStatus.PASSED_AWAY

    vaccination_roll = random.random()
    if vaccination_roll <= vaccination_values["complete_rate"]:
        vaccination_status = DogVaccinationStatus.COMPLETE
    elif vaccination_roll <= vaccination_values["complete_rate"] + vaccination_values["incomplete_rate"]:
        vaccination_status = DogVaccinationStatus.INCOMPLETE
    elif vaccination_roll <= vaccination_values["complete_rate"] + vaccination_values["incomplete_rate"] + vaccination_values["not_vaccinated_rate"]:
        vaccination_status = DogVaccinationStatus.NOT_VACCINATED
    else:
        vaccination_status = DogVaccinationStatus.UNSPECIFIED

    intake_roll = random.random()
    if intake_roll <= intake_values["intake_rate"]:
        intake_reason = DogIntakeStatus.RESCUE
    elif intake_roll <= intake_values["intake_rate"] + intake_values["training_rate"]:
        intake_reason = DogIntakeStatus.TRAINING
    else:
        intake_reason = DogIntakeStatus.HOTEL
    
    owner = None
    if intake_reason != DogIntakeStatus.RESCUE and create_owners: 
        owner = get_random_contact()
        owner.save()

    dog = Dog(
            name=name,
            age_months=age_months,
            gender=gender,
            breed=breed,
            microchip_status=microchip_status,
            microchip_id=microchip_id,
            intake_status=intake_reason,
            arrival_date=arrival_date,
            charter=charter,
            owner=owner,
            current_weight_kg=round(weight, 1),
            height_cm=round(height, 1),
            color=color,
            detailed_description=random.choice(DOG_DESCRIPTIONS),
            health_status=health_status,
            vaccination_status=vaccination_status,
            castration_status=castration_status,
            health_record=random.choice(DOG_HEALTH_RECORDS),
            vaccination_record="DHPP, Rabies, Bordetella - all current",
            treatment_record="***test health record***",
            special_needs=random.choice(DOG_SPECIAL_NEEDS),
            behavioral_notes=random.choice(DOG_BEHAVIORAL_NOTES),
            other_notes=f"***test dog***",
            created=timezone.now(),
            modified=timezone.now()
    )
    return dog


    
CHARTER_NAMES = [
    'TEST KRES_ISTANBUL',
    'TEST KRES_BANDIRMA',
    'TEST KRES_ANKARA',
    'TEST KRES_IZMIR',
    'TEST KRES_ANTALYA',
    'TEST KRES_BURSA',
    'TEST KRES_DENIZLI',
    'TEST KRES_KONYA',
    'TEST KRES_KAYSERI',
    'TEST KRES_MALATYA',
    'TEST KRES_SAMSUN',
    'TEST KRES_SINOP',
    'TEST KRES_TEKIRDAG',
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