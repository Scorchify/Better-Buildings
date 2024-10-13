from django import forms
from .models import Area, Report, BugReport, Announcement

class AreaForm(forms.ModelForm):
    class Media:
        css = {
            "all": ["css/input.css"]
        }
    class Meta:
        model = Area
        fields = ['text']
        labels = {'text': ''}
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter area text here',
                'cols': 40,
                'rows': 5,
            }),
        }

class ReportForm(forms.ModelForm):
    class Media:
        css = {
            "all": ["bootstrap/css/bootstrap.min.css",
                    "css/bs-theme-overrides.css",
                    "css/untitled.css"]
        }
    area = forms.ModelChoiceField(
        queryset=Area.objects.all().distinct(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Report
        fields = ['text', 'area']
        labels = {'text': ''}
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter report text here',
                'cols': 80,
                'rows': 5,
            }),
        }

class BugReportForm(forms.ModelForm):
    class Media:
        css = {
              "all": ["bootstrap/css/bootstrap.min.css",
                    "css/bs-theme-overrides.css",
                    "css/untitled.css"]
        }

    class Meta:
        model = BugReport
        fields = ['text']
        labels = {'text': ''}
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter bug-related info here',
                'cols': 80,
                'rows': 3,
            })
        }

class AnnouncementForm(forms.ModelForm):
    class Media:
        css = {
            "all": ["css/input.css"]
        }
    class Meta:
        model = Announcement
        fields = ['text']
        labels = {'text': ''}
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter area text here',
                'cols': 40,
                'rows': 5,
            }),
        }