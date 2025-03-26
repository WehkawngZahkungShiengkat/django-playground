from django.urls import path
from . import views

app_name = 'maplayers'

urlpatterns = [
    path('', views.map_view, name='map-layers'),
    path('orgstructure/', views.org_struction_direct_html, name='org-structure'),
]
