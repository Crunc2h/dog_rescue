from datetime import datetime
from django.db import models
from django.utils.html import format_html
# Create your models here.


class Owner(models.Model):
    date_registered = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        super(Owner, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class DogGender(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
    UNSPECIFIED = 'U', 'Unspecified'

class DogBreed(models.TextChoices):
    STREET_DOG = 'D', 'Street Dog'

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
class DogVaccinationStatus(models.TextChoices):
    NOT_VACCINATED = 'N', 'Not Vaccinated'
    INCOMPLETE = 'I', 'Incomplete'
    COMPLETE = 'C', 'Complete'


class Dog(models.Model):
    date_registered = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # General Info
    name = models.CharField(max_length=100)
    gender = models.CharField(choices=DogGender.choices, max_length=2, default=DogGender.UNSPECIFIED)
    breed = models.CharField(choices=DogBreed.choices, max_length=2, default=DogBreed.STREET_DOG)
    age = models.IntegerField()
    intake_reason = models.CharField(choices=DogIntakeReasons.choices, max_length=2)
    arrival_date = models.DateTimeField(default=datetime.now)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT)
    microchip_id = models.CharField(max_length=10, blank=True, null=True)

    #Physical Description
    weight_kg = models.FloatField()
    height_cm = models.FloatField()
    color = models.CharField(choices=DogColor.choices, max_length=2)
    detailed_description = models.TextField(blank=True)

    # Health Info
    health_status = models.CharField(choices=DogHealthStatus.choices, max_length=2, default=DogHealthStatus.HEALTHY)
    vaccination_status = models.CharField(choices=DogVaccinationStatus.choices, max_length=2, default=DogVaccinationStatus.NOT_VACCINATED)
    castrated = models.BooleanField(default=False)
    health_record = models.TextField(blank=True)

    # Other
    notes = models.TextField(blank=True)

    def image_tag(self):
        if self.photo:
            return format_html('<img src="{}" width="150" height="150" />', self.photo.url)
        return "No Image"
    image_tag.short_description = 'Image'

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        super(Dog, self).save(*args, **kwargs)





