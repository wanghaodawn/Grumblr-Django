# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0002_auto_20150925_0354'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 25, 4, 22, 47, 174403, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
