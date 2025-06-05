from django.contrib import admin
from django.urls import path
from apk import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.menu_awal, name='menu_awal'),
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('home/<int:user_id>/', views.home, name='home'),
    path('kalkulator/', views.kalkulator, name='kalkulator'),
    path('profil/<int:user_id>/', views.profil, name='profil'),
    path('edukasi/', views.edukasi, name='edukasi'),
    path('logout/', views.logout, name='logout'),
    path('catatan/<int:user_id>/', views.catatan, name='catatan'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
