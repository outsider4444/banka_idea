# Generated by Django 4.1.1 on 2022-09-21 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banka_idea', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='best_solution',
            field=models.BooleanField(default=False, verbose_name='Лучший ответ'),
        ),
    ]
