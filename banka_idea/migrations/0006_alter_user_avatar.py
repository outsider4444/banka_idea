# Generated by Django 4.1.1 on 2022-10-03 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banka_idea', '0005_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='user/base_avatar.png', upload_to='user/avatar', verbose_name='Аватар'),
        ),
    ]