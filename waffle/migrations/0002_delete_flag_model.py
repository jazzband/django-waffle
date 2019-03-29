# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waffle', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flag',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='flag',
            name='users',
        ),
        migrations.AlterField(
            model_name='switch',
            name='active',
            field=models.BooleanField(default=False, help_text='Is this switch active?'),
        ),
        migrations.DeleteModel(
            name='Flag',
        ),
    ]
