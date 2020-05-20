# Generated by Django 3.0.6 on 2020-05-20 02:03

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_auto_20200519_1648'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Address', 'Address'), ('Email', 'Email'), ('Phone', 'Phone')], max_length=50, verbose_name='Contact type')),
                ('content', ckeditor.fields.RichTextField(verbose_name='Content')),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('url', models.CharField(help_text='Example /about/ -page url', max_length=50, verbose_name='Url')),
                ('position', models.CharField(choices=[('Header', 'Header'), ('Footer', 'Footer'), ('Both', 'Both'), ('Useful Links', 'Useful Links')], max_length=50, verbose_name='Position')),
                ('ordering', models.PositiveIntegerField(default=1, verbose_name='Ordering')),
                ('target_blank', models.BooleanField(default=False, help_text='Opens the linked document / page in a new tab', verbose_name='Target blank function')),
            ],
            options={
                'verbose_name': 'Menu',
                'verbose_name_plural': 'Menus',
                'ordering': ('ordering',),
            },
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('comment_date',), 'verbose_name': 'Comment', 'verbose_name_plural': 'Comments'},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ('date_created',), 'verbose_name': 'Task', 'verbose_name_plural': 'Tasks'},
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_content',
            field=models.TextField(verbose_name='Comment content'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Comment date'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Task', verbose_name='Task'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Username'),
        ),
        migrations.AlterField(
            model_name='permitted_user',
            name='comment_allowed_users',
            field=models.ManyToManyField(blank=True, related_name='comment_allowed_users', to=settings.AUTH_USER_MODEL, verbose_name='Comment-allowed users'),
        ),
        migrations.AlterField(
            model_name='permitted_user',
            name='read_only_users',
            field=models.ManyToManyField(blank=True, related_name='read_only_users', to=settings.AUTH_USER_MODEL, verbose_name='Read-only users'),
        ),
        migrations.AlterField(
            model_name='permitted_user',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Task', verbose_name='Task'),
        ),
        migrations.AlterField(
            model_name='task',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='task',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Deadline'),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=ckeditor.fields.RichTextField(max_length=300, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Title'),
        ),
    ]
