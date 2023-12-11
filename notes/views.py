from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from .forms import NoteForm, MeetingForm
from .models import Note, Meeting

def calculate_next_meeting_date(meeting, current_time):
    # Adjust this function to calculate the next meeting date based on frequency
    if meeting.frequency == 'daily':
        while meeting.time <= current_time:
            meeting.time += timedelta(days=1)
    elif meeting.frequency == 'weekly':
        while meeting.time <= current_time:
            meeting.time += timedelta(weeks=1)
    # Add other frequency cases as required
    return meeting.time

@login_required
def home(request):
    note_form = NoteForm()
    meeting_form = MeetingForm()
    edit_meeting = None

    if request.method == 'POST':
        if 'note_submit' in request.POST:
            note_form = NoteForm(request.POST)
            if note_form.is_valid():
                note = note_form.save(commit=False)
                note.user = request.user
                note.save()
                return redirect('home')

        elif 'meeting_submit' in request.POST:
            meeting_id = request.POST.get('meeting_id')
            if meeting_id:
                edit_meeting = get_object_or_404(Meeting, id=meeting_id, user=request.user)
                meeting_form = MeetingForm(request.POST, instance=edit_meeting)
            else:
                meeting_form = MeetingForm(request.POST)

            if meeting_form.is_valid():
                meeting = meeting_form.save(commit=False)
                if not edit_meeting:
                    meeting.user = request.user
                meeting.save()
                return redirect('home')

    last_notes = Note.objects.filter(user=request.user).order_by('-created_at')[:5]
    saved_meetings = Meeting.objects.filter(user=request.user)

    current_time = timezone.now()
    next_meeting = None
    for meeting in saved_meetings:
        next_meeting_date = calculate_next_meeting_date(meeting, current_time)
        if not next_meeting or next_meeting_date < next_meeting.time:
            next_meeting = meeting

    context = {
        'note_form': note_form,
        'meeting_form': meeting_form,
        'edit_meeting': edit_meeting,
        'last_notes': last_notes,
        'next_meeting': next_meeting,
        'saved_meetings': saved_meetings
    }

    return render(request, 'index.html', context)

@login_required
def edit_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id, user=request.user)
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
    meeting = get_object_or_404(Meeting, id=meeting_id, user=request.user)
    meeting.delete()
    return redirect('home')

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Meeting
from django.contrib.auth.decorators import login_required

@login_required
def get_meeting_data(request, meeting_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        meeting = get_object_or_404(Meeting, id=meeting_id, user=request.user)
        meeting_data = {
            'id': meeting.id,
            'name': meeting.name,
            'time': meeting.time.strftime('%Y-%m-%dT%H:%M'),
            'frequency': meeting.frequency
        }
        return JsonResponse(meeting_data)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
