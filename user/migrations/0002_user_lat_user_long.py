# Generated by Django 5.1.5 on 2025-01-19 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='lat',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=9),
        ),
        migrations.AddField(
            model_name='user',
            name='long',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=9),
        ),
    ]
