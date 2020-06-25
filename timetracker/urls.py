"""timetracker URL Configuration

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
from django.contrib import admin
from django.urls import path

from tasks.views import index, start_session, end_current_session

urlpatterns = [
    path('', index, name='index'),
    path('start_session/<int:task_id>/', start_session, name='start_session'),
    path('end_current_session/', end_current_session, name='end_current_session'),

    path('admin/', admin.site.urls),
]
