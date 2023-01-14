from django import forms
import datetime
from django.core.exceptions import ValidationError


class SearchForm(forms.Form):
    keyword = forms.CharField(
        required=True,
        label="Keyword",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter search term",
                "style": "color: red;",
            }
        ),
    )
    start_date = forms.DateField(required=True, help_text="MM/DD/YYYY")
    # start_date= forms.DateField(required=True, widget=forms.SelectDateWidget(), help_text="MM/DD/YYYY")
    end_date = forms.DateField(
        required=True,
        help_text="MM/DD/YYYY",
        error_messages={"required": "Please enter a start date."},
    )
    use_demo_key = forms.ChoiceField(
        choices=[
            (True, "Use demo API key (download limit: 10 articles)"),
            (False, "Enter personal API key (no download limit)"),
        ],
        label="API Mode",
        widget=forms.Select(
            {
                "ng-change": "ChangeDemoStatus()",
                "ng-model": "myValue",
                "ng-init": "True",
            }
        ),
    )
    download_limit = forms.IntegerField(
        required=False, min_value=1, widget=forms.NumberInput(attrs={"ng-if": "!demo"})
    )
    api_key = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"ng-if": "!demo"})
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
