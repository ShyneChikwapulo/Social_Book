from django.urls import path
from . import views
from .views import proxy_news

urlpatterns = [
    path('', views.index, name='index'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('like-post', views.like_post, name='like-post'),
    path('login-or-register', views.login_or_register, name='login_or_register'),
    path('logout', views.logout, name='logout'),
    path('api/news/', proxy_news, name='proxy_news'),
    path('Library', views.Library, name='Library'),
    path('book.html', views.Book, name='book.html'),
    
   
]