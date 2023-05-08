"""
URL configuration for chatbot_project project.

OpenAI based chatbot booking example
Author : Romain Leclerc
Original repo : https://github.com/RomainLLC/booking-openai-chatbot

"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('chat/', include('chatbot_voice.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)