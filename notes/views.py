from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from .forms import NoteForm, MeetingForm
from .models import Note, Meeting

def get_next_occurrence(meeting):
    if meeting.frequency == 'daily':
        return meeting.time + timedelta(days=1)
    elif meeting.frequency == 'weekly':
        return meeting.time + timedelta(weeks=1)
    elif meeting.frequency == 'fortnightly':
        return meeting.time + timedelta(weeks=2)
    elif meeting.frequency == 'monthly':
        return meeting.time + timedelta(weeks=4)
    return None  # For 'one_time' or any other cases

@login_required
def home(request):
    note_form = NoteForm()
    meeting_form = MeetingForm()

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
                return redirect('home')

    last_notes = Note.objects.order_by('-created_at')[:5]

    # Calculate the next meeting
    upcoming_meetings = Meeting.objects.filter(time__gt=timezone.now())
    closest_meeting = None
    closest_time = None
    for meeting in upcoming_meetings:
        next_time = get_next_occurrence(meeting)
        if next_time and (closest_time is None or next_time < closest_time):
            closest_meeting = meeting
            closest_time = next_time
    print("Next meeting:", closest_meeting.time if closest_meeting else "No meeting")

    context = {
        'note_form': note_form,
        'meeting_form': meeting_form,
        'last_notes': last_notes,
        'next_meeting': closest_meeting,
    }

    return render(request, 'index.html', context)
