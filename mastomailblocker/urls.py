"""
URL configuration for mastomailblocker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from app.views import HomeView, FaqView, get_code, DisclaimerView, ImprintView

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('faq/', FaqView.as_view(), name='faq'),
    path('disclaimer/', DisclaimerView.as_view(), name='disclaimer'),
    path('imprint/', ImprintView.as_view(), name='imprint'),
    path('get_code/<int:client_id>/', get_code, name='get_code')
]
