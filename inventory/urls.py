"""inventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.urls import path, include

from . import settings
from .views import dashboard
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import ChangePasswordView

urlpatterns = [
    path('management/', admin.site.urls, name='management'),
    path('', dashboard, name='dashboard'),
    path('store/', include('store.urls')),
    path('api/', include('api.urls')),
    path('pos/', include('pos.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),

]

# urls.py
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = 'Mender POS'
admin.site.site_title = 'Mender POS'
