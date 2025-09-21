from django import forms
from .models import Dog, Contact, Charter


class DogForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = [
            'name', 'age_months', 'photo', 'gender', 'breed',
            'microchip_status', 'microchip_id', 'intake_reason',
            'charter', 'owner', 'is_adopted', 'is_available_for_adoption',
            'adoption_date', 'weight_kg', 'height_cm', 'color',
            'detailed_description', 'health_status', 'vaccination_status',
            'castration_status', 'health_record', 'vaccination_record',
            'treatment_record', 'special_needs', 'behavioral_notes', 'other_notes'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Dog name'}),
            'age_months': forms.NumberInput(attrs={'class': 'form-input', 'min': '0', 'placeholder': 'Age in months'}),
            'photo': forms.FileInput(attrs={'class': 'form-input', 'accept': 'image/*'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'breed': forms.Select(attrs={'class': 'form-select'}),
            'microchip_status': forms.Select(attrs={'class': 'form-select'}),
            'microchip_id': forms.TextInput(
                attrs={'class': 'form-input', 'placeholder': 'Microchip ID (if applicable)'}),
            'intake_reason': forms.Select(attrs={'class': 'form-select'}),
            'charter': forms.Select(attrs={'class': 'form-select'}),
            'owner': forms.Select(attrs={'class': 'form-select'}),
            'adoption_date': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'weight_kg': forms.NumberInput(
                attrs={'class': 'form-input', 'step': '0.1', 'min': '0', 'placeholder': 'Weight in kg'}),
            'height_cm': forms.NumberInput(
                attrs={'class': 'form-input', 'step': '0.1', 'min': '0', 'placeholder': 'Height in cm'}),
            'color': forms.Select(attrs={'class': 'form-select'}),
            'detailed_description': forms.Textarea(
                attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Physical description...'}),
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
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make some fields not required initially
        self.fields['microchip_id'].required = False
        self.fields['owner'].required = False
        self.fields['adoption_date'].required = False

        # Add empty option for optional selects
        self.fields['owner'].empty_label = "No owner assigned"

        # Add helpful help text
        self.fields['age_months'].help_text = "Age in months (e.g., 6 for 6 months old)"
        self.fields['weight_kg'].help_text = "Weight in kilograms"
        self.fields['height_cm'].help_text = "Height in centimeters"


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['charter', 'name', 'email', 'phone', 'address', 'notes']
        widgets = {
            'charter': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone number'}),
            'address': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Full address'}),
            'notes': forms.Textarea(
                attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Additional notes (optional)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['notes'].required = False


class CharterForm(forms.ModelForm):
    class Meta:
        model = Charter
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Charter organization name',
                'maxlength': '100'
            }),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        # Check for duplicate charter names (case-insensitive)
        if Charter.objects.filter(name__iexact=name).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError("A charter with this name already exists.")
        return name.strip().title()  # Clean and format the name