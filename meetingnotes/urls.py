from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')), 
    path('', include('notes.urls')),  # Include the `notes_app` URLs
    # You can add more paths or include other apps' URLs here
]
