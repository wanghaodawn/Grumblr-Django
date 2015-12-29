# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0006_auto_20151012_0449'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('op', models.CharField(max_length=3, choices=[(b'add', b'add')])),
                ('post', models.ForeignKey(to='grumblr.Post')),
            ],
        ),
    ]
