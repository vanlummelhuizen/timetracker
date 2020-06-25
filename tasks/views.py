from django.shortcuts import render, redirect
from django.utils import timezone

from tasks.models import Task, Session, Note


def index(request):
    """
    
    :param request: 
    :return: 
    """
    tasks = Task.objects.filter(project__user=request.user)
    current_sessions = Session.objects.filter(task__project__user=request.user, end__isnull=True)
    if len(current_sessions) > 1:
        pass  #TODO
    elif not current_sessions:
        current_task = None
        notes = None
    else:
        current_task = current_sessions[0].task
        notes = Note.objects.filter(task=current_task)
    return render(request, 'tasks/index.html', {'tasks': tasks, 'current_task': current_task, 'notes': notes})


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


def end_current_session(request):
    """
    
    :param request: 
    :return: 
    """
    # Determine now
    now = timezone.now()

    # End all open session(s)
    open_sessions = Session.objects.filter(task__project__user=request.user, end__isnull=True)
    open_sessions.update(end=now)

    return redirect('index')
