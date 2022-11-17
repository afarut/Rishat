# Generated by Django 4.0.2 on 2022-11-17 16:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('description', models.TextField()),
                ('price', models.PositiveIntegerField(default=50, validators=[django.core.validators.MinValueValidator(50)])),
            ],
        ),
    ]
