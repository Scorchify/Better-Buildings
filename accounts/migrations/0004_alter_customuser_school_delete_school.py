# Generated by Django 4.2.14 on 2024-08-25 04:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('better_buildings', '0007_alter_area_text'),
        ('accounts', '0003_school_customuser_school'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='better_buildings.school'),
        ),
        migrations.DeleteModel(
            name='School',
        ),
    ]