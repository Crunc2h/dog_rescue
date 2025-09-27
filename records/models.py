from django.core.checks import Info
from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

PHOTOS = 'photos/'
DOCUMENTS = 'documents/'

class TripleChoice(models.TextChoices):
    YES = 'Y', 'Yes'
    NO = 'N', 'No'
    UNSPECIFIED = 'U', 'Unspecified'
class DogGender(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
    UNSPECIFIED = 'U', 'Unspecified'
class DogBreed(models.TextChoices):
    STREET_DOG = 'D', 'Street Dog'
    MIXED = 'MIXED', 'Mixed Breed'
    GOLDEN_RETRIEVER = 'GOLDEN', 'Golden Retriever'
    GERMAN_SHEPHERD = 'GERMAN', 'German Shepherd'
    LABRADOR = 'LAB', 'Labrador Retriever'
    BEAGLE = 'BEAGLE', 'Beagle'
    BULLDOG = 'BULL', 'Bulldog'
    PITBULL = 'PIT', 'Pit Bull'
    HUSKY = 'HUSKY', 'Siberian Husky'
    CHIHUAHUA = 'CHI', 'Chihuahua'
    POMERANIAN = 'POM', 'Pomeranian'
    OTHER = 'OTHER', 'Other'
class DogIntakeStatus(models.TextChoices):
    RESCUE = 'R', 'Rescue'
    TRAINING = 'T', 'Training'
    HOTEL = 'H', 'Hotel'
class DogColor(models.TextChoices):
    BLACK = 'B', 'Black'
    WHITE = 'W', 'White'
    GRAY = 'G', 'Gray'
    BROWN = 'BR', 'Brown'
    TAN = 'T', 'Tan'
    CREAM = 'C', 'Cream'
    GOLDEN = 'GOLD', 'Golden'
    RED = 'R', 'Red'
    BLUE = 'BL', 'Blue'
    MULTI_COLOR = 'MC', 'Multi-Color'
    SPOTTED = 'SP', 'Spotted'
    STRIPED = 'ST', 'Striped'
class DogHealthStatus(models.TextChoices):
    HEALTHY = 'H', 'Healthy'
    SICK = 'S', 'Sick'
    PASSED_AWAY = 'P', 'Passed Away'
    UNSPECIFIED = 'U', 'Unspecified'
class DogVaccinationStatus(models.TextChoices):
    NOT_VACCINATED = 'N', 'Not Vaccinated'
    INCOMPLETE = 'I', 'Incomplete'
    COMPLETE = 'C', 'Complete'
    UNSPECIFIED = 'U', 'Unspecified'




class EntityInfo(models.Model):
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.name = self.name.title()
            self.created = timezone.now()
        self.modified = timezone.now()
        super().save(*args, **kwargs)
    
    def clean(self):
        if not self.email and not self.phone:
            raise ValidationError('Email or phone is required')
        if EntityInfo.objects.filter(name=self.name).exists():
            raise ValidationError(f'Name {self.name} already exists')
        if self.email and EntityInfo.objects.filter(email=self.email).exists():
            raise ValidationError(f'Email {self.email} already exists')
        if self.phone and EntityInfo.objects.filter(phone=self.phone).exists():
            raise ValidationError(f'Phone {self.phone} already exists')
    def __str__(self):
        return self.name


class Charter(models.Model):
    entity_info = models.OneToOneField(EntityInfo, on_delete=models.PROTECT)



class Contact(models.Model):
    entity_info = models.OneToOneField(EntityInfo, on_delete=models.PROTECT)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.entity_info.name



class Dog(models.Model):
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()
    
    owner = models.ForeignKey(Contact, on_delete=models.PROTECT, related_name='dogs', blank=True, null=True)
    charter = models.ForeignKey(Charter, on_delete=models.PROTECT, related_name='housed_dogs')

    name = models.CharField(max_length=64)
    age_months = models.IntegerField()

    gender = models.CharField(choices=DogGender.choices, max_length=32, default=DogGender.UNSPECIFIED)
    breed = models.CharField(choices=DogBreed.choices, max_length=32, default=DogBreed.STREET_DOG)

    microchip_status = models.CharField(choices=TripleChoice.choices, max_length=32, default=TripleChoice.UNSPECIFIED)
    microchip_id = models.CharField(max_length=32, blank=True, null=True)

    intake_status = models.CharField(choices=DogIntakeStatus.choices, max_length=32, default=DogIntakeStatus.RESCUE)
    arrival_date = models.DateTimeField(default=timezone.now)
    
    passing_date = models.DateTimeField(blank=True, null=True)
    passing_reason = models.TextField(blank=True, null=True)
    burial_place = models.TextField(blank=True, null=True)

    #Physical Description
    current_weight_kg = models.FloatField(blank=True, null=True)
    height_cm = models.FloatField()
    color = models.CharField(choices=DogColor.choices, max_length=32)
    detailed_description = models.TextField(blank=True)
    
    # Default photo for the dog
    default_photo = models.ImageField(upload_to=PHOTOS, blank=True, null=True, help_text="Default photo for this dog")

    # Health Info
    health_status = models.CharField(choices=DogHealthStatus.choices, max_length=32, default=DogHealthStatus.UNSPECIFIED)
    vaccination_status = models.CharField(choices=DogVaccinationStatus.choices, max_length=32, default=DogVaccinationStatus.UNSPECIFIED)
    castration_status = models.CharField(choices=TripleChoice.choices, max_length=32, default=TripleChoice.UNSPECIFIED)

    health_record = models.TextField(blank=True, default="Any sickness, injuries, pregnancies, castration or other procedures should be entered here.")
    vaccination_record = models.TextField(blank=True, default="The name of the vaccines alongside of the date they were administered should be entered here")
    treatment_record = models.TextField(blank=True, default="Any medication or treatment, with names, dosages and frequency should be entered here")

    # Other
    special_needs = models.TextField(blank=True)
    behavioral_notes = models.TextField(blank=True)
    other_notes = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    @property
    def display_photo(self):
        """
        Returns the best available photo for this dog.
        Priority: profile photo from DogPhotoRecord -> first photo -> default photo
        """
            
        profile_photo = self.photos.filter(is_profile_photo=True).first()
        if profile_photo and profile_photo.photo:
            return profile_photo.photo
        
        first_photo = self.photos.filter(photo__isnull=False).first()
        if first_photo and first_photo.photo:
            return first_photo.photo

        if self.default_photo:
            return self.default_photo
        
        return '/static/images/default-dog.png'
    
    def save(self, *args, **kwargs):
        is_new = not self.id
        if is_new:
            self.name = self.name.title()
            self.created = timezone.now()
        self.modified = timezone.now()

        super().save(*args, **kwargs)
        
        if is_new and self.current_weight_kg:
            self.weight_history.create(weight_kg=self.current_weight_kg)

    def clean(self):
        if self.microchip_status == TripleChoice.YES and not self.microchip_id:
            raise ValidationError('Microchip ID is required when microchip state is Yes')
        if Dog.objects.filter(microchip_id=self.microchip_id).exists():
            raise ValidationError('Microchip ID already exists')
        if self.intake_status == DogIntakeStatus.TRAINING or self.intake_status == DogIntakeStatus.HOTEL and not self.owner:
            raise ValidationError('Owner is required if the dog is being trained')


        if self.health_status == DogHealthStatus.PASSED_AWAY:
            if not self.passing_date:
                raise ValidationError('Passing date is required if the dog is passed away')
            if not self.passing_reason:
                raise ValidationError('Passing reason is required if the dog is passed away')
            if not self.burial_place:
                raise ValidationError('Burial place is required if the dog is passed away')
        
        """
        # Check for duplicate dog names within the same charter.
        # Only allow duplicate names if the other dog with the same name has passed away.
        matching_dogs = self.charter.dogs.filter(name=self.name)
        for match in matching_dogs:
            if match.id != self.id and match.health_status != DogHealthStatus.PASSED_AWAY:
                raise ValidationError('Dog with this name already exists')
        """
        
class DogWeightRecord(models.Model):
    record_date = models.DateTimeField(default=timezone.now)
    weight_kg = models.FloatField()
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name='weight_history')
    
    class Meta:
        ordering = ['-record_date']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.dog:
            self.dog.current_weight_kg = self.weight_kg
            self.dog.save(update_fields=['current_weight_kg'])
    def clean(self):
        if self.weight_kg <= 0:
            raise ValidationError('Weight must be greater than 0')
    def __str__(self):
        return f"{self.dog.name} - {self.weight_kg} kg - {self.record_date:%d-%m-%Y}"


class DogPhotoRecord(models.Model):
    uploaded = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=64)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to=PHOTOS, blank=True, null=True)
    is_profile_photo = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.dog.name} - {self.name}"

    class Meta:
        ordering = ['-is_profile_photo', 'uploaded']
    
class DogDocumentRecord(models.Model):
    uploaded = models.DateTimeField(auto_now_add=True)
    
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to=DOCUMENTS)
    
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    
    
    class Meta:
        ordering = ['-uploaded']
    
    def __str__(self):
        return f"{self.dog.name} - {self.title}"