from django import forms
from .models import Dog, Contact, Charter, Adoptee, EntityInfo, DogAdoptionRecord


class DogForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = [
            'name', 'age_months', 'gender', 'breed',
            'microchip_status', 'microchip_id', 'intake_reason',
            'charter', 'owner', 'eligible_for_adoption', 'adoption_status',
            'current_weight_kg', 'height_cm', 'color',
            'detailed_description', 'default_photo', 'health_status', 'vaccination_status',
            'castration_status', 'health_record', 'vaccination_record',
            'treatment_record', 'special_needs', 'behavioral_notes', 'other_notes',
            'passing_date', 'passing_reason', 'burial_place'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Dog name'}),
            'age_months': forms.NumberInput(attrs={'class': 'form-input', 'min': '0', 'placeholder': 'Age in months'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'breed': forms.Select(attrs={'class': 'form-select'}),
            'microchip_status': forms.Select(attrs={'class': 'form-select'}),
            'microchip_id': forms.TextInput(
                attrs={'class': 'form-input', 'placeholder': 'Microchip ID (if applicable)'}),
            'intake_reason': forms.Select(attrs={'class': 'form-select'}),
            'charter': forms.Select(attrs={'class': 'form-select'}),
            'owner': forms.Select(attrs={'class': 'form-select'}),
            'eligible_for_adoption': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'adoption_status': forms.Select(attrs={'class': 'form-select'}),
            'current_weight_kg': forms.NumberInput(
                attrs={'class': 'form-input', 'step': '0.1', 'min': '0', 'placeholder': 'Current weight in kg'}),
            'height_cm': forms.NumberInput(
                attrs={'class': 'form-input', 'step': '0.1', 'min': '0', 'placeholder': 'Height in cm'}),
            'color': forms.Select(attrs={'class': 'form-select'}),
            'detailed_description': forms.Textarea(
                attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Physical description...'}),
            'default_photo': forms.FileInput(attrs={'class': 'form-input', 'accept': 'image/*'}),
            'health_status': forms.Select(attrs={'class': 'form-select'}),
            'vaccination_status': forms.Select(attrs={'class': 'form-select'}),
            'castration_status': forms.Select(attrs={'class': 'form-select'}),
            'health_record': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'vaccination_record': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'treatment_record': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'special_needs': forms.Textarea(
                attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Any special needs...'}),
            'behavioral_notes': forms.Textarea(
                attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Behavioral observations...'}),
            'other_notes': forms.Textarea(
                attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Additional notes...'}),
            'passing_date': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'passing_reason': forms.Textarea(
                attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Reason for passing...'}),
            'burial_place': forms.TextInput(
                attrs={'class': 'form-input', 'placeholder': 'Burial location...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make some fields not required initially
        self.fields['microchip_id'].required = False
        self.fields['owner'].required = False
        self.fields['current_weight_kg'].required = False
        self.fields['passing_date'].required = False
        self.fields['passing_reason'].required = False
        self.fields['burial_place'].required = False

        # Add empty option for optional selects
        self.fields['owner'].empty_label = "No owner assigned"

        # Add helpful help text
        self.fields['age_months'].help_text = "Age in months (e.g., 6 for 6 months old)"
        self.fields['current_weight_kg'].help_text = "Current weight in kilograms"
        self.fields['height_cm'].help_text = "Height in centimeters"


class ContactForm(forms.ModelForm):
    # EntityInfo fields
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full name'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'email@example.com'}))
    phone = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone number'}))
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Full address'}))

    class Meta:
        model = Contact
        fields = ['entity_info']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.entity_info:
            self.fields['name'].initial = self.instance.entity_info.name
            self.fields['email'].initial = self.instance.entity_info.email
            self.fields['phone'].initial = self.instance.entity_info.phone
            self.fields['address'].initial = self.instance.entity_info.address

    def save(self, commit=True):
        contact = super().save(commit=False)
        
        # Create or update EntityInfo
        if contact.entity_info:
            entity_info = contact.entity_info
        else:
            entity_info = EntityInfo()
        
        entity_info.name = self.cleaned_data['name']
        entity_info.email = self.cleaned_data['email']
        entity_info.phone = self.cleaned_data['phone']
        entity_info.address = self.cleaned_data['address']
        
        if commit:
            entity_info.save()
            contact.entity_info = entity_info
            contact.save()
        
        return contact


class CharterForm(forms.ModelForm):
    # EntityInfo fields
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Charter organization name',
        'maxlength': '100'
    }))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'email@example.com'}))
    phone = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone number'}))
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Organization address'}))

    class Meta:
        model = Charter
        fields = ['entity_info']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.entity_info:
            self.fields['name'].initial = self.instance.entity_info.name
            self.fields['email'].initial = self.instance.entity_info.email
            self.fields['phone'].initial = self.instance.entity_info.phone
            self.fields['address'].initial = self.instance.entity_info.address

    def clean_name(self):
        name = self.cleaned_data['name']
        # Check for duplicate charter names (case-insensitive)
        existing_charters = Charter.objects.filter(entity_info__name__iexact=name)
        if self.instance and self.instance.pk:
            existing_charters = existing_charters.exclude(pk=self.instance.pk)
        if existing_charters.exists():
            raise forms.ValidationError("A charter with this name already exists.")
        return name.strip().title()  # Clean and format the name

    def save(self, commit=True):
        charter = super().save(commit=False)
        
        # Create or update EntityInfo
        if charter.entity_info:
            entity_info = charter.entity_info
        else:
            entity_info = EntityInfo()
        
        entity_info.name = self.cleaned_data['name']
        entity_info.email = self.cleaned_data['email']
        entity_info.phone = self.cleaned_data['phone']
        entity_info.address = self.cleaned_data['address']
        
        if commit:
            entity_info.save()
            charter.entity_info = entity_info
            charter.save()
        
        return charter


class AdopteeForm(forms.ModelForm):
    # EntityInfo fields
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full name'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'email@example.com'}))
    phone = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone number'}))
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Full address'}))

    class Meta:
        model = Adoptee
        fields = ['charter', 'adoption_status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.entity_info:
            self.fields['name'].initial = self.instance.entity_info.name
            self.fields['email'].initial = self.instance.entity_info.email
            self.fields['phone'].initial = self.instance.entity_info.phone
            self.fields['address'].initial = self.instance.entity_info.address

    def save(self, commit=True):
        adoptee = super().save(commit=False)
        
        # Create or update EntityInfo
        if adoptee.entity_info:
            entity_info = adoptee.entity_info
        else:
            entity_info = EntityInfo()
        
        entity_info.name = self.cleaned_data['name']
        entity_info.email = self.cleaned_data['email']
        entity_info.phone = self.cleaned_data['phone']
        entity_info.address = self.cleaned_data['address']
        
        if commit:
            entity_info.save()
            adoptee.entity_info = entity_info
            adoptee.save()
        
        return adoptee


class DogAdoptionRecordForm(forms.ModelForm):
    class Meta:
        model = DogAdoptionRecord
        fields = ['adoptee', 'dog', 'result', 'notes', 'start_date', 'end_date']
        widgets = {
            'adoptee': forms.Select(attrs={'class': 'form-select'}),
            'dog': forms.Select(attrs={'class': 'form-select'}),
            'result': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Adoption process notes...'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['notes'].required = False
        self.fields['start_date'].required = False
        self.fields['end_date'].required = False