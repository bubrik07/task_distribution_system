from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task, TaskStatus, TaskPriority, Executor
from .serializers import (
    TaskSerializer,
    TaskStatusSerializer,
    TaskPrioritySerializer,
    TaskUpdateSerializer,
    ExecutorSerializer,
    ExecutorUpdateSerializer,
)


# Task statuses & priorities -------------------------------------------------------------------------------------------
@api_view(['GET'])
def get_task_statuses(request):
    if request.method == 'GET':
        task_statuses = TaskStatus.objects.all()
        serializer = TaskStatusSerializer(task_statuses, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_task_priorities(request):
    if request.method == 'GET':
        task_priorities = TaskPriority.objects.all()
        serializer = TaskPrioritySerializer(task_priorities, many=True)
        return Response(serializer.data)


# Tasks ----------------------------------------------------------------------------------------------------------------
@api_view(['POST'])
def create_task(request):
    if request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


@api_view(['GET'])
def get_tasks(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


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
@api_view(['POST'])
def create_executor(request):
    if request.method == 'POST':
        serializer = ExecutorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


@api_view(['GET'])
def get_executors(request):
    if request.method == 'GET':
        executors = Executor.objects.all()
        serializer = ExecutorSerializer(executors, many=True)
        return Response(serializer.data)


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
