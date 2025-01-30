from django.db import models


class Executor(models.Model):
    # class Meta:
    #     db_table = "executor"

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, unique=True)
    max_tasks = models.PositiveIntegerField()

    def __str__(self):
        return self.title

    @property
    def task_count(self):
        return self.tasks.count()


class TaskStatus(models.Model):
    # class Meta:
    #     db_table = "task_status"

    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class TaskPriority(models.Model):
    # class Meta:
    #     db_table = "task_priority"

    id = models.AutoField(primary_key=True)
    rank = models.PositiveIntegerField(unique=True)
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Task(models.Model):
    class Meta:
        # db_table = "task"
        ordering = ['priority', 'created_at']

    # STATUS_CHOICES = [
    #     ('pending', 'Pending'),
    #     ('in_progress', 'In Progress'),
    #     ('completed', 'Completed'),
    # ]
    #
    # PRIORITY_CHOICES = [
    #     (1, 'Highest'),
    #     (2, 'High'),
    #     (3, 'Medium'),
    #     (4, 'Low'),
    #     (5, 'Lowest'),
    # ]

    id = models.AutoField(primary_key=True)
    description = models.TextField()
    # priority = models.IntegerField(choices=PRIORITY_CHOICES)
    # status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.ForeignKey(TaskPriority, on_delete=models.CASCADE)
    status = models.ForeignKey(TaskStatus, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    executor = models.ForeignKey(Executor, related_name='tasks', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Task {self.id} - {self.status} - {self.description}"

    def is_completed(self):
        return self.status == 'completed'
