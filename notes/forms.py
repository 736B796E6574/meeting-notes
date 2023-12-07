from django import forms
from .models import Note, Meeting

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['meeting', 'title', 'text']



class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['name', 'time', 'frequency']
        widgets = {
            'time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

