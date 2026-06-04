from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    path('', views.home, name = 'home'),
    path('topics/', views.topics, name='topics'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),
]