from django.urls import path
from . import views

urlpatterns = [
    # Task statuses & priorities
    path('tasks/statuses/', views.get_task_statuses, name='get_task_statuses'),
    path('tasks/priorities/', views.get_task_priorities, name='get_task_priorities'),

    # Tasks
    path('tasks/', views.create_task, name='create_task'),
    path('tasks/list/', views.get_tasks, name='get_tasks'),
    path('tasks/<int:pk>/', views.get_task, name='get_task'),
    path('tasks/<int:pk>/update/', views.update_task, name='update_task'),
    path('tasks/<int:pk>/delete/', views.delete_task, name='delete_task'),
]
