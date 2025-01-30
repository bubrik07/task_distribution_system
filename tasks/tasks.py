from uuid import uuid4
from celery import shared_task

from task_distribution_system.celery import logger
from tasks.models import Task, Executor, TaskStatus
from django.db.models import QuerySet, F, Count


@shared_task
def distribute_tasks():
    logger.info("Distributing tasks...")

    # Get pending status
    pending_status: TaskStatus | None = TaskStatus.objects.get(code='pending')

    # Get all tasks with status 'pending', ordered by priority (highest priority first)
    pending_tasks: QuerySet[Task] = Task.objects.filter(  # noqa
        status=pending_status
    ).order_by('-priority').select_related('status', 'priority', 'executor')
    pending_task_count = pending_tasks.count()

    # Get all executors, sorted by the number of tasks they have
    executors: QuerySet[Executor] = Executor.objects.annotate(  # noqa
        task_count=Count('tasks')
    ).filter(task_count__lt=F('max_tasks')).order_by('task_count')

    for task in pending_tasks:
        # Check if there is an available executor with fewer tasks than their max_tasks limit
        available_executor = None
        for executor in executors:
            if executor.task_count < executor.max_tasks:  # noqa
                available_executor = executor
                break

        if available_executor:
            # Assign the task to the available executor
            task.executor = available_executor
            task.status = TaskStatus.objects.get(code='in_progress')
            task.save()
        else:
            # If no executors are available, stop processing tasks for now
            break

    # Check if the number of tasks in the queue exceeds 10
    if pending_task_count > 10:
        # Generate a unique name for the new executor
        unique_title = f"Executor_{uuid4().hex[:16]}"

        # Ensure the unique_title is not already taken
        while Executor.objects.filter(title=unique_title).exists():
            unique_title = f"Executor_{uuid4().hex[:16]}"  # Regenerate the name if it already exists

        # Add a new executor if there are more than 10 tasks in the queue
        Executor.objects.create(title=unique_title, max_tasks=2)

    # Check if the number of tasks in the queue is less than 5
    elif pending_task_count < 5:
        # Reduce the number of executors to 2 if there are fewer than 5 tasks in the queue
        if Executor.objects.count() > 2:
            least_loaded_executor = Executor.objects.annotate(task_count=Count('tasks')).order_by('task_count').first()
            if least_loaded_executor and least_loaded_executor.task_count == 0:  # noqa
                least_loaded_executor.delete()
