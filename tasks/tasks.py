from celery import shared_task
from tasks.models import Task, Executor, TaskStatus
from django.db.models import QuerySet


@shared_task
def distribute_tasks():
    # Get all tasks with status 'pending', ordered by priority (highest priority first)
    pending_tasks = Task.objects.filter(status='pending').order_by('-priority')

    # Get all executors, sorted by the number of tasks they have
    executors = Executor.objects.all().annotate(task_count=F('tasks__count')).order_by('task_count')

    for task in pending_tasks:
        # Check if there is an available executor with fewer tasks than their max_tasks limit
        available_executor = None
        for executor in executors:
            if executor.task_count < executor.max_tasks:
                available_executor = executor
                break

        if available_executor:
            # Assign the task to the available executor
            task.executor = available_executor
            task.status = 'in_progress'
            task.save()
        else:
            # If no executors are available, stop processing tasks for now
            break

    # Check if the number of tasks in the queue exceeds 10
    if pending_tasks.count() > 10:
        # Add a new executor if there are more than 10 tasks in the queue
        Executor.objects.create(name="New Executor")

    # Check if the number of tasks in the queue is less than 5
    if pending_tasks.count() < 5:
        # Reduce the number of executors to 2 if there are fewer than 5 tasks in the queue
        if Executor.objects.count() > 2:
            # Delete the executor with the fewest tasks (i.e., the one at the end of the list)
            Executor.objects.order_by('-task_count').last().delete()
