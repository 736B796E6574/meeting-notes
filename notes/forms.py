from django import forms
from .models import Note, Meeting

from django import forms
from .models import Note, Meeting
from django.utils import timezone

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['meeting', 'title', 'text']

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        
        # Set placeholders and hide labels
        self.fields['meeting'].widget.attrs.update({'placeholder': 'Meeting'})
        self.fields['title'].widget.attrs.update({'placeholder': 'Title'})
        self.fields['text'].widget.attrs.update({'placeholder': 'Text'})

        # Hide labels
        for field in self.fields:
            self.fields[field].label = False

        # Set the default meeting
        last_meeting = Meeting.objects.filter(time__lte=timezone.now()).order_by('-time').first()
        if last_meeting:
            self.fields['meeting'].initial = last_meeting

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['name', 'time', 'frequency']
        widgets = {
            'time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

