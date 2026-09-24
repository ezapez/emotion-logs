from django import forms 

from .models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['date', 'emotion', 'experience']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'experience': forms.Textarea(attrs={'rows': 5}),
        }