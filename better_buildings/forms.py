from django import forms

from .models import Area, Report

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
    area = forms.ModelChoiceField(Area.objects.all())
    
    class Meta:
        model = Report
        fields = ['text']
        labels = {'text': ''}
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80}),
        }