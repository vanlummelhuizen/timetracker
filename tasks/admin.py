from django.contrib import admin
from tasks.models import *


class ProjectAdmin(admin.ModelAdmin):
    pass
admin.site.register(Project, ProjectAdmin)


class TaskAdmin(admin.ModelAdmin):
    pass
admin.site.register(Task, TaskAdmin)


class NoteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Note, NoteAdmin)


class SessionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Session, SessionAdmin)
