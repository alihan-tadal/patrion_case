# Generated by Django 5.0 on 2023-12-25 11:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="factory",
            name="user",
        ),
        migrations.AddField(
            model_name="user",
            name="factory",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.factory",
            ),
        ),
    ]
