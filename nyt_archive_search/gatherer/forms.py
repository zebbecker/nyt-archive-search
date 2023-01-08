from django import forms
import datetime
from django.core.exceptions import ValidationError


class SearchForm(forms.Form):
    keyword=forms.CharField(required=True, label="Keyword")
    """ start_date= forms.DateField(required=True)
    end_date=forms.DateField(required=True)
    api_key=forms.CharField(required=False)
    download_limit = forms.IntegerField(required=True, initial=10) """
    """ keyword = forms.TextField( blank=False, label="Keyword")# help_text="Enter keyword search term.", required=True, label="Keyword")
    start_date = forms.DateInput(required=True, label="Start date")
    end_date = forms.DateInput(required=True, label="End date")
    api_key = forms.TextInput(help_text = "Enter API key here", required=False, label="API key", initial="")
    download_limit = forms.IntegerField(required=False, label="Download limit", initial=10) """

    def clean_start_date(self):
        data = self.cleaned_data['start_date']
        if data > datetime.date.today():
            raise ValidationError('Invalid date - cannot search future dates.')
        return data

    def clean_end_date(self):
        data = self.cleaned_data['end_date']
        if data > self.cleaned_data['start_date']:
            raise ValidationError("Invalid date range - start date must be before end date.")
        return data