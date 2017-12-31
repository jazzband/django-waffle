# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waffle', '0002_auto_20161201_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='flag',
            name='allow_override',
            field=models.NullBooleanField(default=None),
        ),
    ]
