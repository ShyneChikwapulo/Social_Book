from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.messages_page, name='messages'),
    path('index', views.index, name='index'),
    path('create_thread_api/', views.create_thread_api, name='create_thread_api'),
    
    

]