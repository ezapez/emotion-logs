from django.urls import path

from .import views

app_name = 'emotion_logs'
urlpatterns = [
    path('', views.index, name='index'),
    path('entries/', views.entries, name='entries'),
    path('new-entry/', views.new_entry, name='new_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]