# Generated by Django 4.2.17 on 2024-12-26 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_room_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='message',
            table='message',
        ),
    ]
