from django import forms
from .models import Permit, PermitType, ParkingTicket, Vehicle, Area, ParkingSection
from datetime import date

class PermitForm(forms.ModelForm):
    # Declare the custom form fields here
    duration_days = forms.IntegerField(
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 3'})
    )
    
    # Declare duration_months explicitly too
    duration_months = forms.IntegerField(
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 6'})
    )

    class Meta:
        model = Permit
        fields = [
            "permit_type",
            "owner_name",
            "start_date",
            "duration_days",
            "duration_months",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "owner_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter owner name"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # The rest of your __init__ method is correct and will now work for both fields.
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

        self.fields["duration_days"].required = False
        self.fields["duration_months"].required = False

        permit_type = None

        if "permit_type" in self.data:
            try:
                permit_type_id = int(self.data.get("permit_type"))
                permit_type = PermitType.objects.get(pk=permit_type_id)
            except (ValueError, PermitType.DoesNotExist):
                pass
        elif self.instance and self.instance.pk and self.instance.permit_type:
            permit_type = self.instance.permit_type

        if permit_type:
            if permit_type.is_daily:
                self.fields["duration_days"].widget.attrs["style"] = ""
                self.fields["duration_months"].widget.attrs["style"] = "display:none;"
            elif permit_type.is_monthly:
                self.fields["duration_months"].widget.attrs["style"] = ""
                self.fields["duration_days"].widget.attrs["style"] = "display:none;"
            else:
                self.fields["duration_days"].widget.attrs["style"] = "display:none;"
                self.fields["duration_months"].widget.attrs["style"] = "display:none;"
        else:
            self.fields["duration_days"].widget.attrs["style"] = "display:none;"
            self.fields["duration_months"].widget.attrs["style"] = "display:none;"

    def clean(self):
        # Your clean method is already perfect for this setup.
        cleaned_data = super().clean()
        permit_type = cleaned_data.get("permit_type")

        if permit_type:
            if permit_type.is_daily:
                days = cleaned_data.get("duration_days")
                if not days or days < 1:
                    self.add_error("duration_days", "Please enter a valid number of days")
                cleaned_data["duration_months"] = None
            elif permit_type.is_monthly:
                months = cleaned_data.get("duration_months")
                if not months or months < 1:
                    self.add_error("duration_months", "Please enter a valid number of months")
                cleaned_data["duration_days"] = None
            else:
                cleaned_data["duration_days"] = None
                cleaned_data["duration_months"] = None
        return cleaned_data

class ParkingTicketForm(forms.ModelForm):
    plate_number = forms.CharField(
        label="Vehicle Info",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "e.g., Harrier KCB 124B"
        })
    )

    vehicle_type = forms.ChoiceField(
        choices=Vehicle.VEHICLE_CHOICES,
        label="Vehicle Type",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    # Auto-filled display-only fields
    town_display = forms.CharField(
        label="Town",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"})
    )
    area_display = forms.CharField(
        label="Area",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"})
    )

    class Meta:
        model = ParkingTicket
        fields = [
            "plate_number", "vehicle_type",
            "duration", "time_unit",
            "custom_place"  # Only actual model fields
        ]
        widgets = {
            "duration": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "time_unit": forms.Select(attrs={"class": "form-select"}),
            "custom_place": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "If parking outside designated section"
            }),
        }

    def __init__(self, *args, **kwargs):
        section = kwargs.pop("section", None)
        super().__init__(*args, **kwargs)

        if section:
            self.fields["town_display"].initial = section.area.town.name
            self.fields["area_display"].initial = section.area.name
