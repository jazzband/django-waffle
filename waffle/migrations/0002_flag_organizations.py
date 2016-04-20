# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150918_0947'),
        ('waffle', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flag',
            name='organizations',
            field=models.ManyToManyField(help_text='Activate this flag for these organizations.', to='accounts.Company', blank=True),
        ),
    ]
