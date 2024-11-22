# Generated by Django 4.2.9 on 2024-11-22 06:01

import django.core.files.storage
from django.db import migrations, models
import file.upload_path


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('file', models.FileField(storage=django.core.files.storage.FileSystemStorage(), upload_to=file.upload_path.get_upload_path, verbose_name='file')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
