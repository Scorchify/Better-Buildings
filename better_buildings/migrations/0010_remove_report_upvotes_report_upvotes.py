# Generated by Django 4.2.14 on 2024-08-03 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('better_buildings', '0009_remove_report_upvotes_report_upvotes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='upvotes',
        ),
        migrations.AddField(
            model_name='report',
            name='upvotes',
            field=models.IntegerField(default=0),
        ),
    ]