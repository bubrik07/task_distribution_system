from django.urls import path
from tasks import views

urlpatterns = [
    # Task statuses & priorities
    path('tasks/statuses/', views.get_task_statuses, name='get_task_statuses'),
    path('tasks/priorities/', views.get_task_priorities, name='get_task_priorities'),

    # Tasks
    path('tasks/', views.create_task, name='create_task'),
    path('tasks/<int:pk>/', views.get_task, name='get_task'),
    path('tasks/list', views.get_tasks, name='get_tasks'),
    path('tasks/<int:pk>/update/', views.update_task, name='update_task'),

    # Executors
    path('executors/', views.create_executor, name='create_executor'),
    path('executors/<int:pk>/', views.get_executor, name='get_executor'),
    path('executors/list', views.get_executors, name='get_executors'),
    path('executors/<int:pk>/update/', views.update_executor, name='update_executor'),

    # Monitoring
    path('monitoring/tasks/', views.get_task_statistics, name='get_task_statistics'),

]
