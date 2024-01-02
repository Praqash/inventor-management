# Generated by Django 5.0 on 2024-01-01 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invmanage", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="producttype",
            name="name",
            field=models.CharField(
                help_text="Required",
                max_length=255,
                unique=True,
                verbose_name="Product Type",
            ),
        ),
    ]
