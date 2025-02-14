# Generated by Django 2.2 on 2022-09-28 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ndf', '0004_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='assigned_project',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='assigned_subject',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
