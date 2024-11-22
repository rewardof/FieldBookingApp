# Generated by Django 4.2.9 on 2024-11-22 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('start_time', models.DateTimeField(help_text='The start time of the booking.')),
                ('end_time', models.DateTimeField(help_text='The end time of the booking.')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('Cancelled', 'Cancelled'), ('Completed', 'Completed')], default='Pending', help_text='The current status of the booking.', max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
