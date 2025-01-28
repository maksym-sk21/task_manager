from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from .models import Project, Task
from .forms import ProjectForm, TaskForm
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        projects = Project.objects.filter(user=request.user)
        return render(request, "index.html", {'projects': projects})
    else:
        return render(request, "index.html")


@login_required
def project_list(request):
    projects = Project.objects.filter(user=request.user).order_by("id")
    return render(request, "project_list.html", {"projects": projects})


@login_required
@require_POST
@csrf_exempt
def project_create(request):
    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save(commit=False)
        project.user = request.user
        project.save()
        projects = Project.objects.filter(user=request.user)
        return render(request, "project_list.html", {"projects": projects})
    return JsonResponse({"errors": form.errors}, status=400)


@login_required
@csrf_exempt
def project_update(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            projects = Project.objects.filter(user=request.user).order_by("id")
            return render(request, "project_list.html", {"projects": projects})
        return JsonResponse({"errors": form.errors}, status=400)
    else:
        form = ProjectForm(instance=project)
        return render(request, "project_item.html", {"form": form, "project": project})


@login_required
@require_http_methods(["DELETE"])
@csrf_exempt
def project_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    project.delete()
    projects = Project.objects.filter(user=request.user)
    return render(request, "project_list.html", {"projects": projects})


@login_required
def task_list(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    tasks = Task.objects.filter(project_id=project_id)
    return render(request, "task_list.html", {"tasks": tasks, "project": project})


@login_required
@require_POST
@csrf_exempt
def task_create(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    form = TaskForm(request.POST)
    if form.is_valid():
        task = form.save(commit=False)
        task.project = project
        task.save()
        tasks = Task.objects.filter(project=project)
        return render(request, "task_list.html", {"tasks": tasks, "project": project})
    return JsonResponse({"errors": form.errors}, status=400)


@login_required
@csrf_exempt
def task_update(request, project_id, task_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            tasks = Task.objects.filter(project=project)
            return render(request, "task_list.html", {"tasks": tasks, "project": project})
        return JsonResponse({"errors": form.errors}, status=400)
    else:
        form = TaskForm(instance=task)
        return render(request, "task_item.html", {"form": form, "task": task, "project": project})


@login_required
@require_http_methods(["DELETE"])
@csrf_exempt
def task_delete(request, project_id, task_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    tasks = Task.objects.filter(project_id=project_id)
    return render(request, "task_list.html", {"tasks": tasks, "project": project})


@login_required
@csrf_exempt
def task_priority_up(request, project_id, task_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    task = get_object_or_404(Task, id=task_id, project=project)
    prev_task = Task.objects.filter(
        project=project, priority__lt=task.priority
    ).order_by('-priority').first()

    if prev_task:
        task.priority, prev_task.priority = prev_task.priority, task.priority
        task.save()
        prev_task.save()
    tasks = Task.objects.filter(project=project)
    return render(request, "task_list.html", {"tasks": tasks, "project": project})


@login_required
@csrf_exempt
def task_priority_down(request, project_id, task_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    task = get_object_or_404(Task, id=task_id, project=project)
    next_task = Task.objects.filter(
        project=project, priority__gt=task.priority
    ).order_by('priority').first()

    if next_task:
        task.priority, next_task.priority = next_task.priority, task.priority
        task.save()
        next_task.save()
    tasks = Task.objects.filter(project=project)
    return render(request, "task_list.html", {"tasks": tasks, "project": project})


@login_required
@csrf_exempt
def task_status_toggle(request, project_id, task_id):
    task = get_object_or_404(Task, id=task_id, project__id=project_id)
    task.status = not task.status
    task.save()
    tasks = Task.objects.filter(project=task.project)
    return render(request, "task_list.html", {"tasks": tasks, "project": task.project})
