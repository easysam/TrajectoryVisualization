from django.urls import path
from . import views

app_name='map'
urlpatterns = [
    path('', views.index, name='index'),
    path('ce_trajectory', views.ce_trajectory_data, name='ce_trajectory'),
]