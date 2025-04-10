from django.urls import path
from . import views

app_name = 'maplayers'

urlpatterns = [
    path('', views.MapClassView2.as_view(), name='map-layers'),
    path('simple/', views.map_view, name='map-layers-simple'),
    path('2/', views.map_view2, name='map-layers2'),
    path('orgstructure/', views.org_struction_direct_html, name='org-structure'),
    path('class/', views.MapClassView.as_view(), name="map-layer-class"),
    path('class2/', views.MapClassView2.as_view(), name="map-layer-class-2"),
    path('class3/', views.MapClassView3.as_view(), name="map-layer-class-3")
]
