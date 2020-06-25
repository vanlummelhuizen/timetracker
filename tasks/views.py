from django.shortcuts import render

from tasks.models import Task


def index(request):
    """
    
    :param request: 
    :return: 
    """
    tasks = Task.objects.filter(project__user=request.user)
    return render(request, 'tasks/index.html', {'tasks': tasks})
