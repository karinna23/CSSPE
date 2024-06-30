from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'admin_mode'

urlpatterns = [
    path('referees', views.referees, name="referees"),
    path('add_referee', views.add_referee, name="add_referee"),
]