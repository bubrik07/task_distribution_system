from rest_framework import serializers
from .models import Task, Executor, TaskStatus, TaskPriority


class TaskPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskPriority
        fields = ['id', 'rank', 'code', 'title']


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = ['id', 'code', 'title']


class ExecutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Executor
        fields = ['id', 'title', 'max_tasks']


class TaskSerializer(serializers.ModelSerializer):
    priority = TaskPrioritySerializer()
    status = TaskStatusSerializer()
    executor = ExecutorSerializer()

    class Meta:
        model = Task
        fields = ['id', 'description', 'priority', 'status', 'created_at', 'completed_at', 'executor']

    def create(self, validated_data):
        priority_data = validated_data.pop('priority')
        status_data = validated_data.pop('status')
        executor_data = validated_data.pop('executor')

        priority = TaskPriority.objects.create(**priority_data)
        status = TaskStatus.objects.create(**status_data)
        executor = Executor.objects.create(**executor_data)

        task = Task.objects.create(priority=priority, status=status, executor=executor, **validated_data)
        return task

    def update(self, instance, validated_data):
        priority_data = validated_data.pop('priority', None)
        status_data = validated_data.pop('status', None)
        executor_data = validated_data.pop('executor', None)

        if priority_data:
            priority = instance.priority
            for attr, value in priority_data.items():
                setattr(priority, attr, value)
            priority.save()

        if status_data:
            status = instance.status
            for attr, value in status_data.items():
                setattr(status, attr, value)
            status.save()

        if executor_data:
            executor = instance.executor
            for attr, value in executor_data.items():
                setattr(executor, attr, value)
            executor.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance