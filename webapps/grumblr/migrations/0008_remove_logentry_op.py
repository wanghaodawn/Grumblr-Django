# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0007_logentry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logentry',
            name='op',
        ),
    ]
