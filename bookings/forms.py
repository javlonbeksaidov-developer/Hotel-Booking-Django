from django import forms

from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["check_in", "check_out"]  # noqa: RUF012
        widgets = {  # noqa: RUF012
            "check_in": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "check_out": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")

        if check_in and check_out and check_out <= check_in:
            raise forms.ValidationError(
                "Chiqish sanasi kirish sanasidan keyin bo'lishi kerak."
            )

        return cleaned_data