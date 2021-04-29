# Generated by Django 3.2 on 2021-04-29 22:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publish_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('content', models.TextField()),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('publish_time',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publish_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('content', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_comments', to=settings.AUTH_USER_MODEL)),
                ('comment_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post')),
                ('reply_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='blog.comment')),
            ],
            options={
                'ordering': ('publish_time',),
                'abstract': False,
            },
        ),
    ]
