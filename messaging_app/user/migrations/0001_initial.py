# Generated by Django 5.1 on 2024-08-30 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Users",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=250)),
                ("phone_number", models.CharField(max_length=20)),
                ("email", models.CharField(max_length=100, null=True)),
            ],
            options={
                "db_table": "users",
            },
        ),
    ]
