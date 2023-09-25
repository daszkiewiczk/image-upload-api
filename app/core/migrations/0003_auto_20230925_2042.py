# Generated by Django 3.2.21 on 2023-09-25 20:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_alter_myuser_tier"),
    ]

    operations = [
        migrations.AddField(
            model_name="myuser",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="myuser",
            name="is_staff",
            field=models.BooleanField(default=False),
        ),
    ]
