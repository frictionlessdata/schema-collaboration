# Generated by Django 3.1.4 on 2020-12-01 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_suggestions_from_django_doctor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datapackage',
            name='name',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
    ]