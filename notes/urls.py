from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('edit-meeting/<int:meeting_id>/', views.edit_meeting, name='edit_meeting'),
    path('delete-meeting/<int:meeting_id>/', views.delete_meeting, name='delete_meeting'),
]
