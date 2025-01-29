from django.db import migrations


def add_initial_task_priorities(apps, schema_editor):
    TaskPriority = apps.get_model('tasks', 'TaskPriority')
    TaskPriority.objects.create(rank=1, code='highest', title='Highest')
    TaskPriority.objects.create(rank=2, code='high', title='High')
    TaskPriority.objects.create(rank=3, code='medium', title='Medium')
    TaskPriority.objects.create(rank=4, code='low', title='Low')
    TaskPriority.objects.create(rank=5, code='lowest', title='Lowest')


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_add_initial_task_status'),
    ]

    operations = [
        migrations.RunPython(add_initial_task_priorities),
    ]
