from django import forms
from .models import Permit, Property
# Define the choices for the permit_type field
PERMIT_TYPES = [
    ('single_business', 'Single Business Permit'),
    ('building', 'Building Permit'),
    ('liquor', 'Liquor License'),
    ('advert', 'Advertisement Permit'),
    ('env_health', 'Environmental/Health Permit')
]

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['lr_number', 'location', 'valuation', 'arrears']
        widgets = {
            'lr_number': forms.TextInput(attrs={'class': 'form-input'}),
            'location': forms.TextInput(attrs={'class': 'form-input'}),
            'valuation': forms.NumberInput(attrs={'class': 'form-input'}),
            'arrears': forms.NumberInput(attrs={'class': 'form-input'}),
        }

class PermitForm(forms.ModelForm):
    # CRITICAL: Define permit_type as a field so it can be rendered separately.
    permit_type = forms.ChoiceField(
        choices=PERMIT_TYPES,
        label="Select Permit Type"
    )

    # These custom fields will always be part of the form
    business_name = forms.CharField(max_length=255, required=False, label="Business Name")
    business_type = forms.CharField(max_length=255, required=False, label="Business Type")
    project_name = forms.CharField(max_length=255, required=False, label="Project Name")
    project_address = forms.CharField(max_length=255, required=False, label="Project Address")
    license_type = forms.CharField(max_length=255, required=False, label="License Type")
    premises_address = forms.CharField(max_length=255, required=False, label="Premises Address")

    class Meta:
        model = Permit
        # Now, include all fields (both model and custom) in the fields list.
        # This allows the template loop to work.
        fields = [
            'permit_type', 'fee', 'valid_from', 'valid_to',
            'business_name', 'business_type',
            'project_name', 'project_address',
            'license_type', 'premises_address',
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Assemble the data dictionary from the form's cleaned data
        instance.data = {}
        if instance.permit_type == 'single_business':
            instance.data['business_name'] = self.cleaned_data.get('business_name')
            instance.data['business_type'] = self.cleaned_data.get('business_type')
        elif instance.permit_type == 'building':
            instance.data['project_name'] = self.cleaned_data.get('project_name')
            instance.data['project_address'] = self.cleaned_data.get('project_address')
        elif instance.permit_type == 'liquor':
            instance.data['license_type'] = self.cleaned_data.get('license_type')
            instance.data['premises_address'] = self.cleaned_data.get('premises_address')

        if commit:
            instance.save()
        return instance