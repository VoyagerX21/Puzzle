from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('choices/', views.choices, name='choices'),
    
    # REST / AJAX API endpoints
    path('api/state/', views.api_game_state, name='api_game_state'),
    path('api/move/', views.api_move, name='api_move'),
    path('api/shuffle/', views.api_shuffle, name='api_shuffle'),
    path('api/select-preset/', views.api_select_preset, name='api_select_preset'),
    path('api/upload-photo/', views.api_upload_photo, name='api_upload_photo'),
    path('api/reset/', views.api_reset, name='api_reset'),
    
    # Backwards compatibility
    path('taken/', views.api_select_preset, name='taken'),
]