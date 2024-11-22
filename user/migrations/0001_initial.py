# Generated by Django 4.2.9 on 2024-11-22 06:01

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(db_index=True, max_length=512, unique=True, verbose_name='username')),
                ('full_name', models.CharField(max_length=150, verbose_name='full name')),
                ('email', models.EmailField(blank=True, max_length=128, null=True, verbose_name='email address')),
                ('phone_number', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='phone number')),
                ('language', models.CharField(choices=[('English', 'English'), ('uzbek', 'Uzbek'), ('russian', 'Russian')], default='uzbek', null=True, verbose_name='preferred language')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='date of birth')),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=16, null=True, verbose_name='gender')),
                ('user_type', models.CharField(choices=[('customer', 'Customer'), ('admin', 'Admin'), ('field_owner', 'Field Owner')], default='customer', max_length=15, verbose_name='user type')),
                ('auth_method', models.CharField(choices=[('phone', 'Phone'), ('email', 'Email')], max_length=10, null=True, verbose_name='auth method')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('is_verified', models.BooleanField(default=False, help_text='Designates whether this user is verified.')),
                ('password', models.CharField(max_length=128, null=True, verbose_name='password')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.address', verbose_name='address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='VerificationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('code', models.IntegerField()),
                ('code_type', models.CharField(choices=[('register', 'Register'), ('login', 'Login'), ('forgot_password', 'Forgot Password')], max_length=20)),
                ('expires_at', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
