# Generated by Django 3.2 on 2021-04-21 19:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publish_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('content', models.TextField()),
            ],
            options={
                'ordering': ('publish_time',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publish_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('content', models.TextField()),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'ordering': ('publish_time',),
                'abstract': False,
            },
        ),
    ]
