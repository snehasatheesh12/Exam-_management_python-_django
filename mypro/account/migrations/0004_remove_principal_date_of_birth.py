# Generated by Django 5.1.3 on 2024-11-14 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_principal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='principal',
            name='date_of_birth',
        ),
    ]