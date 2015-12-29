# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grumblr', '0008_remove_logentry_op'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comment_owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('post_owner', models.ForeignKey(to='grumblr.Post')),
            ],
        ),
    ]
