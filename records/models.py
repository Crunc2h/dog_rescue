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
    OTHER = 'OTHER', 'Other'
class DogIntakeReasons(models.TextChoices):
    RESCUE = 'R', 'Rescue'
    TRAINING = 'T', 'Training'
class DogColor(models.TextChoices):
    BLACK = 'B', 'Black'
    WHITE = 'W', 'White'
    GRAY = 'G', 'Gray'
class DogHealthStatus(models.TextChoices):
    HEALTHY = 'H', 'Healthy'
    SICK = 'S', 'Sick'
    PASSED_AWAY = 'P', 'Passed Away'
class DogVaccinationStatus(models.TextChoices):
    NOT_VACCINATED = 'N', 'Not Vaccinated'
    INCOMPLETE = 'I', 'Incomplete'
    COMPLETE = 'C', 'Complete'
    UNSPECIFIED = 'U', 'Unspecified'

class AdoptionStatus(models.TextChoices):
    IDLE = 'I', 'Idle'
    TRIAL = 'T', 'Trial'
    ADOPTED = 'A', 'Adopted'
    NOT_AVAILABLE = 'N', 'Not Available'
class AdoptionResult(models.TextChoices):
    APPROVED = 'A', 'Approved'
    REJECTED = 'R', 'Rejected'
    EVALUATION = 'E', 'Evaluation'


class EntityInfo(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.name = self.name.title()
        super().save(*args, **kwargs)
    
    def clean(self):
        if not self.email and not self.phone:
            raise ValidationError('Email or phone is required')
        if EntityInfo.objects.filter(name=self.name).exists():
            raise ValidationError(f'Name {self.name} already exists')
        if EntityInfo.objects.filter(email=self.email).exists():
            raise ValidationError(f'Email {self.email} already exists')
        if EntityInfo.objects.filter(phone=self.phone).exists():
            raise ValidationError(f'Phone {self.phone} already exists')
    def __str__(self):
        return self.name


class Charter(models.Model):
    entity_info = models.OneToOneField(EntityInfo, on_delete=models.PROTECT)


class Contact(models.Model):
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    entity_info = models.OneToOneField(EntityInfo, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.entity_info.name

class Adoptee(Contact):
    charter = models.ForeignKey(Charter, on_delete=models.PROTECT)
    adoption_status = models.CharField(choices=AdoptionStatus.choices, max_length=32, default=AdoptionStatus.IDLE)


class Dog(models.Model):
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    name = models.CharField(max_length=64)
    age_months = models.IntegerField()

    gender = models.CharField(choices=DogGender.choices, max_length=32, default=DogGender.UNSPECIFIED)
    breed = models.CharField(choices=DogBreed.choices, max_length=32, default=DogBreed.STREET_DOG)

    microchip_status = models.CharField(choices=TripleChoice.choices, max_length=32, default=TripleChoice.UNSPECIFIED)
    microchip_id = models.CharField(max_length=32, blank=True, null=True)

    intake_reason = models.CharField(choices=DogIntakeReasons.choices, max_length=32, default=DogIntakeReasons.RESCUE)
    arrival_date = models.DateTimeField(default=timezone.now)
    
    passing_date = models.DateTimeField(blank=True, null=True)
    passing_reason = models.TextField(blank=True, null=True)
    burial_place = models.TextField(blank=True, null=True)

    charter = models.ForeignKey(Charter, on_delete=models.PROTECT, related_name='dogs')

    #Adoption
    eligible_for_adoption = models.BooleanField(default=False)
    owner = models.ForeignKey(Adoptee, on_delete=models.PROTECT, related_name='adopted_dogs', blank=True, null=True)
    adoption_status = models.CharField(choices=AdoptionStatus.choices, max_length=32, default=AdoptionStatus.NOT_AVAILABLE)

    #Physical Description
    current_weight_kg = models.FloatField(blank=True, null=True)
    height_cm = models.FloatField()
    color = models.CharField(choices=DogColor.choices, max_length=32)
    detailed_description = models.TextField(blank=True)

    # Health Info
    health_status = models.CharField(choices=DogHealthStatus.choices, max_length=32, default=DogHealthStatus.HEALTHY)
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
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.name = self.name.title()
            self.created = timezone.now()
            if self.current_weight_kg:
                self.weight_history.create(weight_kg=self.current_weight_kg)
        
        if self.eligible_for_adoption and self.adoption_status == AdoptionStatus.NOT_AVAILABLE:
            self.adoption_status = AdoptionStatus.IDLE
        elif not self.eligible_for_adoption and self.adoption_status == AdoptionStatus.IDLE:
            self.adoption_status = AdoptionStatus.NOT_AVAILABLE
        
        if self.health_status == DogHealthStatus.PASSED_AWAY:
            self.eligible_for_adoption = False
            self.adoption_status = AdoptionStatus.NOT_AVAILABLE
        self.modified = timezone.now()
        super().save(*args, **kwargs)

    def clean(self):
        if self.microchip_status == TripleChoice.YES and not self.microchip_id:
            raise ValidationError('Microchip ID is required when microchip state is Yes')
        if Dog.objects.filter(microchip_id=self.microchip_id).exists():
            raise ValidationError('Microchip ID already exists')
        if self.health_status == DogHealthStatus.PASSED_AWAY:
            if not self.passing_date:
                raise ValidationError('Passing date is required if the dog is passed away')
            if not self.passing_reason:
                raise ValidationError('Passing reason is required if the dog is passed away')
            if not self.burial_place:
                raise ValidationError('Burial place is required if the dog is passed away')
        
        matching_dogs = self.charter.dogs.filter(name=self.name)
        for match in matching_dogs:
            if match.id != self.id and match.health_status != DogHealthStatus.PASSED_AWAY:
                raise ValidationError('Dog with this name already exists')
        


class DogWeightRecord(models.Model):
    record_date = models.DateTimeField(default=timezone.now)
    weight_kg = models.FloatField()
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name='weight_history')
    
    class Meta:
        ordering = ['-recorded_date']

    def save(self, *args, **kwargs):
        if not self.id:
            self.dog.current_weight_kg = self.dog.weight_history.last().weight_kg
        super().save(*args, **kwargs)
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
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.dog.name} - {self.title}"


class DogAdoptionRecord(models.Model):
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    charter = models.ForeignKey(Charter, on_delete=models.PROTECT, blank=True, null=True)
    adoptee = models.ForeignKey(Adoptee, on_delete=models.PROTECT, related_name='adoptions')
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name='adoptions')
    
    is_active = models.BooleanField(default=True, editable=False)
    result = models.CharField(choices=AdoptionResult.choices, max_length=32, default=AdoptionResult.EVALUATION)
    notes = models.TextField(blank=True)
    
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.charter = self.dog.charter
            self.created = timezone.now()
        self.modified = timezone.now()

        if self.is_active:
            if not self.dog.eligible_for_adoption:
                raise ValidationError('Dog is not eligible for adoption')
            for adoption in self.dog.adoptions.all():
                if adoption.id != self.id and adoption.is_active:
                    raise ValidationError('Dog already has an active adoption process')
            self.update()
        super().save(*args, **kwargs)

    def update(self):
        if self.result == AdoptionResult.EVALUATION:
            if not self.start_date:
                self.start_date = timezone.now()
            self.is_active = True
            
            self.dog.eligible_for_adoption = False
            self.dog.adoption_status = AdoptionStatus.TRIAL

            self.adoptee.adoption_status = AdoptionStatus.TRIAL
        elif self.result == AdoptionResult.APPROVED:
            self.is_active = False
            self.end_date = timezone.now()
            
            self.dog.eligible_for_adoption = False
            self.dog.adoption_status = AdoptionStatus.ADOPTED
            self.dog.owner = self.adoptee
            
            self.adoptee.adoption_status = AdoptionStatus.IDLE
        
        elif self.result == AdoptionResult.REJECTED:
            self.is_active = False
            self.end_date = timezone.now()
            
            self.dog.eligible_for_adoption = True
            self.dog.adoption_status = AdoptionStatus.IDLE

            self.adoptee.adoption_status = AdoptionStatus.IDLE
        self.dog.save()
        self.adoptee.save()




    