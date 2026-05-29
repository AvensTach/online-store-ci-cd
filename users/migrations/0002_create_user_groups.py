from django.db import migrations
from django.contrib.auth.models import Group

def create_groups(apps, schema_editor):
    admin_group, _ = Group.objects.get_or_create(name='admin')
    customer_group, _ = Group.objects.get_or_create(name='customer')

def reverse_groups(apps, schema_editor):
    Group.objects.filter(name__in=['admin', 'customer']).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(create_groups, reverse_groups),
    ]