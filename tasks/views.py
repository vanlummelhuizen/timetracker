from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
import datetime

from tasks.models import Project, Task, Session, Note
from tasks.forms import TaskForm


def get_global_context(request):
    """
    Get the global context for showing the side bar
    :param request: 
    :return: 
    """
    projects = Project.objects.all().prefetch_related('task_set')
    current_sessions = Session.objects.filter(task__project__user=request.user, end__isnull=True)
    if len(current_sessions) > 1:
        pass  # TODO
    elif not current_sessions:
        current_task = None
        notes = None
    else:
        current_task = current_sessions[0].task
        notes = Note.objects.filter(task=current_task)

    today = datetime.date.today()
    recent_sessions = Session.objects.filter(task__project__user=request.user).order_by('-start')[:4:-1]

    return {
        'projects': projects,
        'current_task': current_task,
        'notes': notes,
        'recent_sessions': recent_sessions
    }


def index(request):
    """
    
    :param request: 
    :return: 
    """

    return render(request, 'tasks/index.html', get_global_context(request))


def menu(request):
    context = get_global_context(request)
    return render(request, 'menu.html', context)


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


def add_note(request, task_id):
    """
    
    :param request: 
    :param task_id: 
    :return: 
    """
    if request.method == 'POST':
        if 'note' in request.POST:
            # Get task
            try:
                task = Task.objects.get(pk=task_id)
            except:
                redirect('index')

            note = Note.objects.create(task=task, text=request.POST['note'])
    return redirect('index')


class CreateProject(CreateView):
    model = Project
    fields = ['name']
    template_name = 'generic_form.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_global_context(self.request))
        context['title'] = "Create project"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateProject(UpdateView):
    model = Project
    fields = ['name']
    template_name = 'generic_form.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_global_context(self.request))
        context['title'] = "Update project"
        return context


class CreateTask(CreateView):
    model = Task
    template_name = 'generic_form.html'
    success_url = reverse_lazy('index')
    form_class = TaskForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_global_context(self.request))
        context['title'] = "Create task"
        return context

    def get_form_kwargs(self):
        kwargs = super(CreateTask, self).get_form_kwargs()
        kwargs.update({'user': self.request.user, 'project': self.request.GET.get('project', None)})
        return kwargs


class UpdateTask(UpdateView):
    model = Task
    template_name = 'generic_form.html'
    success_url = reverse_lazy('index')
    form_class = TaskForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_global_context(self.request))
        context['title'] = "Update task"
        return context

    def get_form_kwargs(self):
        kwargs = super(CreateTask, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class UpdateNote(UpdateView):
    model = Note
    template_name = 'generic_form.html'
    success_url = reverse_lazy('index')
    fields = ['text']
