from django.shortcuts import render, redirect
from .forms import NoteForm, MeetingForm
from .models import Note, Meeting
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    # Initialize forms outside of the if-else block
    note_form = NoteForm()
    meeting_form = MeetingForm()
    print(request.POST)
    if request.method == 'POST':
        if 'note_submit' in request.POST:
            note_form = NoteForm(request.POST)
            if note_form.is_valid():
                note_form.save()
                return redirect('home')
        elif 'meeting_submit' in request.POST:
            meeting_form = MeetingForm(request.POST)
            if meeting_form.is_valid():
                meeting_form.save()
                print("Meeting saved")
                return redirect('home')

    last_notes = Note.objects.order_by('-created_at')[:5]
    next_meeting = Meeting.objects.filter(time__gt=timezone.now()).order_by('time').first()

    context = {
        'note_form': note_form,
        'meeting_form': meeting_form,
        'last_notes': last_notes,
        'next_meeting': next_meeting,
    }
    return render(request, 'index.html', context)
