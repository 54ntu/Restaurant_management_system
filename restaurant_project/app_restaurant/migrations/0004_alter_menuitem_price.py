# Generated by Django 5.0.7 on 2024-08-13 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_restaurant', '0003_alter_table_table_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
