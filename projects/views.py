from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from .models import Project, Task
from .forms import ProjectForm, TaskForm
# Create your views here.


def home(request) -> HttpResponse:
    """
    Displays the main page. If the user is logged in,
    shows projects associated with the current user.

    Args:
    request (HttpRequest): HTTP request from the client.

    Returns:
    HttpResponse: The main page with or without projects.
    """
    if request.user.is_authenticated:
        projects = Project.objects.filter(user=request.user)
        return render(request, "index.html", {'projects': projects})
    else:
        return render(request, "index.html")


@login_required
def project_list(request) -> HttpResponse:
    """
    Displays a list of the current user's projects, sorted by id.

    Args:
    request (HttpRequest): HTTP request from the client.

    Returns:
    HttpResponse: Page with the list of projects.
    """
    projects = Project.objects.filter(user=request.user).order_by("id")
    return render(request, "project_list.html", {"projects": projects})


@login_required
@require_POST
@csrf_exempt
def project_create(request) -> HttpResponse | JsonResponse:
    """
    Creates a new project for the current user based on the form data.

    Args:
    request (HttpRequest): HTTP request with form data.

    Returns:
    JsonResponse: Error response if the form is not validated.
    HttpResponse: Project list page if the project was successfully created.
    """
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
def project_update(request, project_id: int) -> HttpResponse | JsonResponse:
    """
    Updates the current user's project data.

    Args:
    request (HttpRequest): HTTP request with form data.
    project_id (int): Project ID to update.

    Returns:
    JsonResponse: Error response if form validation failed.
    HttpResponse: Page with updated project if data saved successfully.
    """
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
def project_delete(request, project_id: int) -> HttpResponse:
    """
    Deletes the current user's project by the given ID.

    Args:
    request (HttpRequest): HTTP request to delete.
    project_id (int): ID of the project to delete.

    Returns:
    HttpResponse: Page with the list of projects after deletion.
    """
    project = get_object_or_404(Project, id=project_id, user=request.user)
    project.delete()
    projects = Project.objects.filter(user=request.user)
    return render(request, "project_list.html", {"projects": projects})


@login_required
def task_list(request, project_id: int) -> HttpResponse:
    """
    Displays a list of tasks for the current user's specified project.

    Args:
    request (HttpRequest): HTTP request from the client.
    project_id (int): The ID of the project to display tasks for.

    Returns:
    HttpResponse: A page with a list of tasks for the project.
    """
    project = get_object_or_404(Project, id=project_id, user=request.user)
    tasks = Task.objects.filter(project_id=project_id)
    return render(request, "task_list.html", {"tasks": tasks, "project": project})


@login_required
@require_POST
@csrf_exempt
def task_create(request, project_id: int) -> HttpResponse | JsonResponse:
    """
    Creates a new task for the given project of the current user.

    Args:
    request (HttpRequest): HTTP request with form data.
    project_id (int): ID of the project to which the task belongs.

    Returns:
    JsonResponse: Error response if the form is not validated.
    HttpResponse: Page with the list of project tasks if the task was successfully created.
    """
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
def task_update(request, project_id: int, task_id: int) -> HttpResponse | JsonResponse:
    """
    Updates a task for the current user's given project.

    Args:
    request (HttpRequest): HTTP request with form data.
    project_id (int): Project ID for the task.
    task_id (int): Task ID to update.

    Returns:
    JsonResponse: Error response if the form fails validation.
    HttpResponse: Page with updated task if data saved successfully.
    """
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
def task_delete(request, project_id: int, task_id: int) -> HttpResponse:
    """
    Deletes a task for the given project of the current user.

    Args:
    request (HttpRequest): HTTP request to delete.
    project_id (int): ID of the project the task belongs to.
    task_id (int): ID of the task to delete.

    Returns:
    HttpResponse: Page with the list of tasks for the project after deletion.
    """
    project = get_object_or_404(Project, id=project_id, user=request.user)
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    tasks = Task.objects.filter(project_id=project_id)
    return render(request, "task_list.html", {"tasks": tasks, "project": project})


@login_required
@csrf_exempt
def task_priority_up(request, project_id: int, task_id: int) -> HttpResponse:
    """
    Increases the priority of a task for the current user's specified project.

    Args:
    request (HttpRequest): HTTP request to change the priority.
    project_id (int): Project ID for the task.
    task_id (int): Task ID to change the priority.

    Returns:
    HttpResponse: Page with the list of tasks for the project after the priority has been changed.
    """""
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
def task_priority_down(request, project_id: int, task_id: int) -> HttpResponse:
    """
    Lowers the priority of a task for the current user's specified project.

    Args:
    request (HttpRequest): HTTP request to change the priority.
    project_id (int): Project ID for the task.
    task_id (int): Task ID to change the priority.

    Returns:
    HttpResponse: Page with the list of tasks for the project after the priority has been changed.
    """
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
def task_status_toggle(request, project_id: int, task_id: int) -> HttpResponse:
    """
    Marks a task as completed for the given project for the current user.

    Args:
    request (HttpRequest): HTTP request to change the task status.
    project_id (int): Project ID for the task.
    task_id (int): Task ID to change the status of.

    Returns:
    HttpResponse: Page with the list of tasks for the project after the task status was changed.
    """
    task = get_object_or_404(Task, id=task_id, project__id=project_id)
    task.status = not task.status
    task.save()
    tasks = Task.objects.filter(project=task.project)
    return render(request, "task_list.html", {"tasks": tasks, "project": task.project})
