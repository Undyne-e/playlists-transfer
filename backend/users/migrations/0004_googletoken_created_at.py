# Generated by Django 5.1.4 on 2025-02-25 17:44

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_googletoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='googletoken',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
