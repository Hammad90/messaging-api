# Generated by Django 5.1 on 2024-08-26 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0001_initial'),
        ('user', '0002_users_chats'),
    ]

    operations = [
        migrations.AddField(
            model_name='groups',
            name='users',
            field=models.ManyToManyField(related_name='user_groups', to='user.users'),
        ),
        migrations.DeleteModel(
            name='UsersGrous',
        ),
    ]
