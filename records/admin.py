from django.contrib import admin
from .models import Dog, Contact, Charter, Adoptee, EntityInfo, DogAdoptionRecord, DogPhotoRecord, DogDocumentRecord, DogWeightRecord
from django.utils.html import format_html
# Register your models here.


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_charter_name', 'get_owner_name', 'arrival_date', 'display_photo_preview']
    search_fields = ['name', 'charter__entity_info__name', 'owner__entity_info__name']
    readonly_fields = ['modified', 'display_photo_preview']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'age_months', 'gender', 'breed', 'color', 'default_photo', 'display_photo_preview')
        }),
        ('Physical Description', {
            'fields': ('current_weight_kg', 'height_cm', 'detailed_description')
        }),
        ('Health Information', {
            'fields': ('health_status', 'vaccination_status', 'castration_status', 'health_record', 'vaccination_record', 'treatment_record')
        }),
        ('Adoption Information', {
            'fields': ('eligible_for_adoption', 'adoption_status', 'owner', 'charter')
        }),
        ('Other Information', {
            'fields': ('special_needs', 'behavioral_notes', 'other_notes', 'passing_date', 'passing_reason', 'burial_place')
        }),
        ('System Information', {
            'fields': ('created', 'modified'),
            'classes': ('collapse',)
        }),
    )
    
    def get_charter_name(self, obj):
        return obj.charter.entity_info.name if obj.charter and obj.charter.entity_info else '-'
    get_charter_name.short_description = 'Charter'
    
    def get_owner_name(self, obj):
        return obj.owner.entity_info.name if obj.owner and obj.owner.entity_info else '-'
    get_owner_name.short_description = 'Owner'
    
    def display_photo_preview(self, obj):
        if obj.display_photo:
            if hasattr(obj.display_photo, 'url'):
                return format_html('<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 5px;" />', obj.display_photo.url)
            else:
                return format_html('<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 5px;" />', obj.display_photo)
        return "No photo"
    display_photo_preview.short_description = 'Photo Preview'

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'created']
    search_fields = ['entity_info__name', 'entity_info__phone', 'entity_info__email']
    readonly_fields = ['modified']
    
    def get_name(self, obj):
        return obj.entity_info.name if obj.entity_info else '-'
    get_name.short_description = 'Name'

@admin.register(Charter)
class CharterAdmin(admin.ModelAdmin):
    list_display = ['get_name']
    search_fields = ['entity_info__name', 'entity_info__phone', 'entity_info__email']
    
    def get_name(self, obj):
        return obj.entity_info.name if obj.entity_info else '-'
    get_name.short_description = 'Name'

@admin.register(Adoptee)
class AdopteeAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'adoption_status', 'created']
    search_fields = ['entity_info__name', 'entity_info__phone', 'entity_info__email']
    readonly_fields = ['modified']
    
    def get_name(self, obj):
        return obj.entity_info.name if obj.entity_info else '-'
    get_name.short_description = 'Name'

@admin.register(EntityInfo)
class EntityInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone']
    search_fields = ['name', 'email', 'phone']

@admin.register(DogAdoptionRecord)
class DogAdoptionRecordAdmin(admin.ModelAdmin):
    list_display = ['dog', 'adoptee', 'result', 'start_date', 'end_date']
    search_fields = ['dog__name', 'adoptee__entity_info__name']
    readonly_fields = ['modified']

@admin.register(DogPhotoRecord)
class DogPhotoRecordAdmin(admin.ModelAdmin):
    list_display = ['dog', 'name', 'is_profile_photo', 'uploaded']
    search_fields = ['dog__name', 'name']
    readonly_fields = ['uploaded']

@admin.register(DogDocumentRecord)
class DogDocumentRecordAdmin(admin.ModelAdmin):
    list_display = ['dog', 'title', 'document_type', 'uploaded']
    search_fields = ['dog__name', 'title', 'document_type']
    readonly_fields = ['uploaded']

@admin.register(DogWeightRecord)
class DogWeightRecordAdmin(admin.ModelAdmin):
    list_display = ['dog', 'weight_kg', 'record_date']
    search_fields = ['dog__name']
    readonly_fields = ['record_date']



