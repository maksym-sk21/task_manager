from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("projects/", views.project_list, name="project_list"),
    path("projects/create/", views.project_create, name="project_create"),
    path("projects/<int:project_id>/update/", views.project_update, name="project_update"),
    path("projects/<int:project_id>/delete/", views.project_delete, name="project_delete"),
    path('project/<int:project_id>/tasks/', views.task_list, name='task_list'),
    path('project/<int:project_id>/task/create/', views.task_create, name='task_create'),
    path("project/<int:project_id>/tasks/update/<int:task_id>/", views.task_update, name="task_update"),
    path("project/<int:project_id>/tasks/delete/<int:task_id>/", views.task_delete, name="task_delete"),
    path('project/<int:project_id>/task/<int:task_id>/priority/up/', views.task_priority_up, name='task_priority_up'),
    path('project/<int:project_id>/task/<int:task_id>/priority/down/',
         views.task_priority_down, name='task_priority_down'),
    path('project/<int:project_id>/task/<int:task_id>/status/toggle/',
         views.task_status_toggle, name='task_status_toggle'),
]
