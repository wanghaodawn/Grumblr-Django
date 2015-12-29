# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0004_info'),
    ]

    operations = [
        migrations.RenameField(
            model_name='info',
            old_name='picture',
            new_name='photo',
        ),
    ]
