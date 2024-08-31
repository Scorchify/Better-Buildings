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
        
class ReportForm(forms.ModelForm):
    class Media:
        css = {
            "all": ["css/input.css"]
        }
    area = forms.ModelChoiceField(
    queryset=Area.objects.all(),
    required=True,
    widget=forms.Select(attrs={'class': 'dropdown-box'})
)

    class Meta:
        model = Report
        fields = ['text', 'area']
        labels = {'text': ''}
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'input-box',
                'placeholder': 'Enter report text here',
                'cols': 80,
                'rows': 5,
            }),
        }

class BugReportForm(forms.ModelForm):
    class Media:
        css = {
            "all": ["css/input.css"]
        }

    class Meta:
        model = BugReport
        fields = ['text']
        labels = {'text': ''}
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'input-box',
                'placeholder': 'Enter bug-related info here',
                'cols': 80,
                'rows': 10,
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
                'class': 'input-box',
                'placeholder': 'Enter announcement text here',
                'cols': 80,
                'rows': 5,
            }),
        }