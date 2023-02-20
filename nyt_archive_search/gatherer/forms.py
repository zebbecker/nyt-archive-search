from django import forms
import datetime
from gatherer.config import NYT_DEFAULT_LIMIT
from django.core.exceptions import ValidationError


class DemoSearchForm(forms.Form):
    keyword = forms.CharField(
        required=True,
        label="Search term",
        widget=forms.TextInput(attrs={"placeholder": "Enter search term here"}),
    )
    start_date = forms.DateField(
        required=True,
        error_messages={"required": "Please enter a start date."},
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    end_date = forms.DateField(
        required=True,
        error_messages={"required": "Please enter an end date."},
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    def clean_start_date(self):
        data = self.cleaned_data["start_date"]
        if data > datetime.date.today():
            raise ValidationError("Invalid date - cannot search future dates.")
        return data

    def clean_end_date(self):
        data = self.cleaned_data["end_date"]
        if data < self.cleaned_data["start_date"]:
            raise ValidationError(
                "Invalid date range - start date must be before end date."
            )
        return data


class FullSearchForm(forms.Form):
    keyword = forms.CharField(
        required=True,
        label="Search term",
        widget=forms.TextInput(attrs={"placeholder": "Enter search term here"}),
    )
    start_date = forms.DateField(
        required=True,
        error_messages={"required": "Please enter a start date."},
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    end_date = forms.DateField(
        required=True,
        error_messages={"required": "Please enter an end date."},
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    download_limit = forms.IntegerField(
        required=False, min_value=1, widget=forms.NumberInput(attrs={})
    )
    api_key = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your NYT Developer API Key here"}
        ),
    )

    user_email = forms.EmailField(
        required=True,
    )

    def clean_start_date(self):
        data = self.cleaned_data["start_date"]
        if data > datetime.date.today():
            raise ValidationError("Invalid date - cannot search future dates.")
        return data

    def clean_end_date(self):
        data = self.cleaned_data["end_date"]
        if data < self.cleaned_data["start_date"]:
            raise ValidationError(
                "Invalid date range - start date must be before end date."
            )
        return data
