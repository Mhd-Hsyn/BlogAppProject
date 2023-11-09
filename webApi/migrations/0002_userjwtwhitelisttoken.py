# Generated by Django 4.2.7 on 2023-11-09 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("webApi", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserJWTWhiteListToken",
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
                ("token", models.TextField(default="")),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "user_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="webApi.user",
                    ),
                ),
            ],
        ),
    ]