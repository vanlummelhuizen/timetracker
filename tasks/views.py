from django.shortcuts import render, redirect
from django.utils import timezone

from tasks.models import Task, Session


def index(request):
    """
    
    :param request: 
    :return: 
    """
    tasks = Task.objects.filter(project__user=request.user)
    current_sessions = Session.objects.filter(task__project__user=request.user, end__isnull=True)
    if len(current_sessions) > 1:
        pass  #TODO
    current_task = current_sessions[0].task
    return render(request, 'tasks/index.html', {'tasks': tasks, 'current_task': current_task})


def start_session(request, task_id):
    """
    
    :param request: 
    :param task_id: 
    :return: 
    """
    # Determine now
    now = timezone.now()

    # Get task
    try:
        task = Task.objects.get(pk=task_id)
    except:
        redirect('index')

    # End open session(s)
    open_sessions = Session.objects.filter(task__project__user=request.user, end__isnull=True)
    open_sessions.update(end=now)

    # Start a new session
    new_session = Session.objects.create(task=task, start=now)

    return redirect('index')