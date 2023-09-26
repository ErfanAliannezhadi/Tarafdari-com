"""Django_Tarafdari_Clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

api_urlpatterns = [
    path('accounts/', include('accounts.api_urls', namespace='api_accounts')),
    path('posts/', include('posts.api_urls', namespace='api_posts')),
    path('statuses/', include('statuses.api_urls', namespace='api_statuses')),
    path('teams/', include('teams', namespace='api_teams')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('teams/', include('teams.urls', namespace='teams')),
    path('status/', include('statuses.urls', namespace='statuses')),
    path('posts/', include('posts.urls', namespace='posts')),
    path('o/', include('social_django.urls', namespace='social')),
    path('api/', include(api_urlpatterns)),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
