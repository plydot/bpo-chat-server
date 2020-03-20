# Generated by Django 2.2.4 on 2020-03-18 20:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField()),
                ('avatar', models.ImageField(upload_to='')),
                ('bio', models.TextField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now=True, null=True)),
                ('date_joined', models.DateTimeField(auto_now=True, null=True)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('phone', models.CharField(max_length=50, unique=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('is_staff', models.BooleanField()),
                ('is_superuser', models.BooleanField()),
            ],
            options={
                'verbose_name_plural': 'Users',
                'db_table': 'users'
            },
        ),
        migrations.CreateModel(
            name='GroupUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'users_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UsersPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'users_user_permissions',
                'managed': False,
            },
        ),
    ]