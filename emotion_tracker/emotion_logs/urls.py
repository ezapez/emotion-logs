from django.urls import path

from .import views

app_name = 'emotion_logs'
urlpatterns = [
    # Home page 
    path('', views.index, name='index'),
    # page with all the notes of the emotion 
    path('topics/', views.topics, name='topics'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    #page for editing an entry
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]