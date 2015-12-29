# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0005_auto_20151012_0343'),
    ]

    operations = [
        migrations.RenameField(
            model_name='info',
            old_name='first_name',
            new_name='firstname',
        ),
        migrations.RenameField(
            model_name='info',
            old_name='last_name',
            new_name='lastname',
        ),
    ]
