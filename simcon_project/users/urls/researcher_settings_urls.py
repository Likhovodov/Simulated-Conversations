from django.urls import path
from users.views import *

app_name = 'settings'
urlpatterns = [
    path('', researcher_settings_view, name="main"),
]
