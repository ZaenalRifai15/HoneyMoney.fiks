from django.contrib import admin
from django.urls import path
from apk import views

urlpatterns = [
    path('', views.menu_awal, name='menu_awal'),
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('home/<int:user_id>/', views.home, name='home'),
]
