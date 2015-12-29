# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grumblr', '0003_post_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(default=b'', max_length=20, blank=True)),
                ('last_name', models.CharField(default=b'', max_length=20, blank=True)),
                ('age', models.CharField(default=b'', max_length=3, blank=True)),
                ('bio', models.CharField(default=b'', max_length=420, blank=True)),
                ('email', models.EmailField(default=b'', max_length=20, blank=True)),
                ('picture', models.ImageField(upload_to=b'photo', blank=True)),
                ('followers', models.ManyToManyField(related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('owner', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
