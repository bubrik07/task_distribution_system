from django.db import migrations


def add_initial_task_statuses(apps, schema_editor):
    TaskStatus = apps.get_model('tasks', 'TaskStatus')
    TaskStatus.objects.create(code='pending', title='Pending')
    TaskStatus.objects.create(code='in_progress', title='In Progress')
    TaskStatus.objects.create(code='completed', title='Completed')


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_initial_task_statuses),
    ]
