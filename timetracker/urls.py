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
from django.urls import path, include
from django.contrib.auth.decorators import login_required

from tasks.views import index, menu, start_session, end_current_session, add_note, CreateProject, UpdateProject, \
    CreateTask, UpdateTask, UpdateNote

urlpatterns = [
    path('', login_required(index), name='index'),
    path('menu', login_required(menu), name='menu'),
    path('start_session/<int:task_id>/', login_required(start_session), name='start_session'),
    path('end_current_session/', login_required(end_current_session), name='end_current_session'),
    path('add_note/<int:task_id>/', login_required(add_note), name='add_note'),
    path('project/create', login_required(CreateProject.as_view()), name='create_project'),
    path('project/update/<int:pk>', login_required(UpdateProject.as_view()), name='update_project'),
    path('task/create', login_required(CreateTask.as_view()), name='create_task'),
    path('task/update/<int:pk>', login_required(UpdateTask.as_view()), name='update_task'),
    path('note/update/<int:pk>', login_required(UpdateNote.as_view()), name='update_note'),

    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]
