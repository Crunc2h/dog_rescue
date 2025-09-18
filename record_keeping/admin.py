from django.contrib import admin
from .models import Dog, Owner
from django.utils.html import format_html
# Register your models here.


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner__name','arrival_date', 'date_updated']
    list_display_links = ['owner__name']
    search_fields = ['name', 'owner__name']

    # Organize form fields
    fieldsets = (
        ('General Information', {
            'fields': ('name', 'intake_reason', 'owner', 'arrival_date', 'gender', 'breed', 'age', 'microchip_id', 'image_tag')
        }),
        ('Physical Description', {
            'fields': ('weight_kg', 'height_cm', 'color', 'detailed_description')
        }),
        ('Health Information', {
            'fields': ('health_status', 'vaccination_status', 'castrated', 'health_record')
        }),
        ('Misc', {
            'fields': ('notes',)
        }),
    )

    readonly_fields = ['image_tag']
@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):

    list_display = ['name', 'date_registered', ]
    search_fields = ['name', 'phone', 'email']



