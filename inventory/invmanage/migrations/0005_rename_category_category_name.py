# Generated by Django 5.0 on 2024-01-01 23:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("invmanage", "0004_rename_name_category_category"),
    ]

    operations = [
        migrations.RenameField(
            model_name="category",
            old_name="category",
            new_name="name",
        ),
    ]
