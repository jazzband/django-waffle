# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('waffle', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flag',
            name='sessions',
            field=models.BooleanField(default=False, help_text=b'Flag is active for session with the required key value'),
            preserve_default=True,
        ),
    ]
