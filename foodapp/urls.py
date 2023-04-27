"""
URL configuration for foodapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from . import views

# for static files and media
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('recipes/', views.recipes, name='recipes'),
    path('recipes/veg/', views.veg, name='veg'),
    path('recipes/nonveg/', views.nonveg, name='nonveg'),
    path('recipes/healthy/', views.healthy, name='healthy'),
    path('search/', views.search, name='search'),
    path('add_comment/<int:bid>', views.add_comment, name='add_comment'),



    path('singleblog/<int:pk>', views.singleblog, name='singleblog'),
    path('accounts/', include('accounts.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
