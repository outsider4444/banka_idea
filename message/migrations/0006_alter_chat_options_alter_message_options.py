# Generated by Django 4.1.1 on 2022-10-06 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0005_remove_message_useravatar'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chat',
            options={'verbose_name': 'Чат', 'verbose_name_plural': 'Чаты'},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('date_added',), 'verbose_name': 'Личное сообщение', 'verbose_name_plural': 'Личные сообщения'},
        ),
    ]