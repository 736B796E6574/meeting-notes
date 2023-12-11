from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from .forms import NoteForm, MeetingForm
from .models import Note, Meeting

def calculate_next_meeting(meeting):
    if meeting.frequency == 'daily':
        return meeting.time + timedelta(days=1)
    elif meeting.frequency == 'weekly':
        return meeting.time + timedelta(weeks=1)
    elif meeting.frequency == 'fortnightly':
        return meeting.time + timedelta(weeks=2)
    elif meeting.frequency == 'monthly':
        return meeting.time + timedelta(weeks=4)
    return meeting.time  # For 'one_time' frequency

@login_required
def home(request):
    note_form = NoteForm()
    meeting_form = MeetingForm()

    if request.method == 'POST':
        if 'note_submit' in request.POST:
            note_form = NoteForm(request.POST)
            if note_form.is_valid():
                note = note_form.save(commit=False)
                note.user = request.user
                note.save()
                return redirect('home')
        elif 'meeting_submit' in request.POST:
            meeting_form = MeetingForm(request.POST)
            if meeting_form.is_valid():
                meeting = meeting_form.save(commit=False)
                meeting.user = request.user
                meeting.save()
                return redirect('home')

    last_notes = Note.objects.filter(user=request.user).order_by('-created_at')[:5]
    saved_meetings = Meeting.objects.filter(user=request.user)

    # Calculate the next upcoming meeting
    next_meeting = None
    for meeting in saved_meetings:
        next_meeting_date = calculate_next_meeting(meeting)
        if next_meeting_date >= timezone.now():
            if next_meeting is None or next_meeting_date < next_meeting.time:
                next_meeting = meeting

    context = {
        'note_form': note_form,
        'meeting_form': meeting_form,
        'last_notes': last_notes,
        'next_meeting': next_meeting,  # Add next_meeting to context
    }

    return render(request, 'index.html', context)

@login_required
def edit_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MeetingForm(instance=meeting)
    return render(request, 'edit_meeting.html', {'form': form})

@login_required
def delete_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    meeting.delete()
    return redirect('home')
