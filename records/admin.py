from django.contrib import admin
from .models import Dog, Contact
from django.utils.html import format_html
# Register your models here.


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ['name', 'charter__name', 'owner__name', 'arrival_date']
    search_fields = ['name', 'charter__name', 'owner__name']
    readonly_fields =  ['modified']

@admin.register(Contact)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', ]
    search_fields = ['name', 'phone', 'email']
    readonly_fields = ['modified']



