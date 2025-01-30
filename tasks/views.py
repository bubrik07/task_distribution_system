from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from tasks.models import Task, TaskStatus, TaskPriority, Executor
from tasks.serializers import (
    TaskSerializer,
    TaskStatusSerializer,
    TaskPrioritySerializer,
    TaskUpdateSerializer,
    ExecutorSerializer,
    ExecutorUpdateSerializer,
)


# Task statuses & priorities -------------------------------------------------------------------------------------------
@swagger_auto_schema(
    operation_description="Retrieve all task statuses",
    responses={200: TaskStatusSerializer(many=True)},
    methods=['GET'],
)
@api_view(['GET'])
def get_task_statuses(request):
    if request.method == 'GET':
        task_statuses = TaskStatus.objects.all()
        serializer = TaskStatusSerializer(task_statuses, many=True)
        return Response(serializer.data)


@swagger_auto_schema(
    operation_description="Retrieve all task priorities",
    responses={200: TaskPrioritySerializer(many=True)},
    methods=['GET'],
)
@api_view(['GET'])
def get_task_priorities(request):
    if request.method == 'GET':
        task_priorities = TaskPriority.objects.all()
        serializer = TaskPrioritySerializer(task_priorities, many=True)
        return Response(serializer.data)


# Tasks ----------------------------------------------------------------------------------------------------------------
@swagger_auto_schema(
    operation_description="Create a new task",
    request_body=TaskSerializer,
    responses={201: TaskSerializer, 400: 'Invalid data'},
    methods=['POST'],
)
@api_view(['POST'])
def create_task(request):
    if request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    operation_description="Retrieve a task by its ID",
    responses={200: TaskSerializer, 404: 'Task not found'},
    methods=['GET'],
)
@api_view(['GET'])
def get_task(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(
            data={"detail": "Task not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)


@swagger_auto_schema(
    operation_description="Retrieve all tasks",
    responses={200: TaskSerializer(many=True)},
    methods=['GET'],
)
@api_view(['GET'])
def get_tasks(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


@swagger_auto_schema(
    operation_description="Update an existing task",
    request_body=TaskUpdateSerializer,
    responses={200: TaskSerializer, 404: 'Task not found', 400: 'Invalid data'},
    methods=['PATCH'],
)
@api_view(['PATCH'])
def update_task(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(
            data={"detail": "Task not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'PATCH':
        serializer = TaskUpdateSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Executors ------------------------------------------------------------------------------------------------------------
@swagger_auto_schema(
    operation_description="Create a new executor",
    request_body=ExecutorSerializer,
    responses={201: ExecutorSerializer, 400: 'Invalid data'},
    methods=['POST'],
)
@api_view(['POST'])
def create_executor(request):
    if request.method == 'POST':
        serializer = ExecutorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    operation_description="Retrieve an executor by its ID",
    responses={200: ExecutorSerializer, 404: 'Executor not found'},
    methods=['GET'],
)
@api_view(['GET'])
def get_executor(request, pk):
    try:
        executor = Executor.objects.get(pk=pk)
    except Executor.DoesNotExist:
        return Response(
            data={"detail": "Executor not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = ExecutorSerializer(executor)
        return Response(serializer.data)


@swagger_auto_schema(
    operation_description="Retrieve all executors",
    responses={200: ExecutorSerializer(many=True)},
    methods=['GET'],
)
@api_view(['GET'])
def get_executors(request):
    if request.method == 'GET':
        executors = Executor.objects.all()
        serializer = ExecutorSerializer(executors, many=True)
        return Response(serializer.data)


@swagger_auto_schema(
    operation_description="Update an existing executor",
    request_body=ExecutorUpdateSerializer,
    responses={200: ExecutorSerializer, 404: 'Executor not found', 400: 'Invalid data'},
    methods=['PATCH'],
)
@api_view(['PATCH'])
def update_executor(request, pk):
    try:
        executor = Executor.objects.get(pk=pk)
    except Executor.DoesNotExist:
        return Response(
            data={"detail": "Executor not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'PATCH':
        serializer = ExecutorUpdateSerializer(executor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Monitoring -----------------------------------------------------------------------------------------------------------
@swagger_auto_schema(
    operation_description="Retrieve task statistics including total count and task status distribution",
    responses={
        200: openapi.Response(
            description='Task Statistics',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'total_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'task_statuses': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'status': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'code': openapi.Schema(type=openapi.TYPE_STRING),
                                        'title': openapi.Schema(type=openapi.TYPE_STRING),
                                    }
                                ),
                                'count': openapi.Schema(type=openapi.TYPE_INTEGER),
                            }
                        )
                    ),
                }
            )
        ),
    },
    methods=['GET'],
)
@api_view(['GET'])
def get_task_statistics(request):
    # Get total count of tasks
    total_count = Task.objects.count()

    all_task_statuses = TaskStatus.objects.all()
    task_statuses = []

    for task_status in all_task_statuses:
        count = Task.objects.filter(status=task_status).count()
        task_statuses.append({
            'status': {
                'id': task_status.id,
                'code': task_status.code,
                'title': task_status.title,
            },
            'count': count
        })

    return Response({
        'total_count': total_count,
        'task_statuses': task_statuses
    })
