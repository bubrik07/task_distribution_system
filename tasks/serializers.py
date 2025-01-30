from rest_framework import serializers
from tasks.models import Task, Executor, TaskStatus, TaskPriority


class TaskPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskPriority
        fields = ['id', 'rank', 'code', 'title']


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = ['id', 'code', 'title']


class BaseExecutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Executor
        fields = ['id', 'title', 'max_tasks']


class TaskSerializer(serializers.ModelSerializer):
    # Приймаємо тільки ID в запиті (через PrimaryKeyRelatedField)
    priority = serializers.PrimaryKeyRelatedField(queryset=TaskPriority.objects.all())
    status = serializers.PrimaryKeyRelatedField(queryset=TaskStatus.objects.all())
    executor = serializers.PrimaryKeyRelatedField(queryset=Executor.objects.all(), required=False)

    # Відповідь буде серіалізувати повні об'єкти
    priority_details = TaskPrioritySerializer(source='priority', read_only=True)
    status_details = TaskStatusSerializer(source='status', read_only=True)
    executor_details = BaseExecutorSerializer(source='executor', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'description', 'priority', 'status', 'created_at', 'completed_at', 'executor', 'priority_details', 'status_details', 'executor_details']


class TaskSerializerWithoutExecutorDetails(serializers.ModelSerializer):
    priority_details = TaskPrioritySerializer(source='priority', read_only=True)
    status_details = TaskStatusSerializer(source='status', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'description', 'priority', 'status', 'created_at', 'completed_at', 'priority_details', 'status_details']


class ExecutorSerializer(BaseExecutorSerializer):
    tasks = TaskSerializerWithoutExecutorDetails(many=True, read_only=True)

    class Meta(BaseExecutorSerializer.Meta):
        fields = BaseExecutorSerializer.Meta.fields + ['tasks']


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status']  # Only status can be updated


class ExecutorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Executor
        fields = ['max_tasks']  # Only max_tasks can be updated
