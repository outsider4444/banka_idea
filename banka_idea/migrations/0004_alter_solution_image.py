# Generated by Django 4.1.1 on 2022-09-11 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banka_idea', '0003_alter_solution_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='image',
            field=models.ImageField(blank=True, upload_to='solutions/'),
        ),
    ]
