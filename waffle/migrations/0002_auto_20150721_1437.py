# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('waffle', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flag',
            name='site',
            field=models.ForeignKey(related_name='waffle_flags', blank=True, to='sites.Site', null=True),
        ),
        migrations.AddField(
            model_name='sample',
            name='site',
            field=models.ForeignKey(related_name='waffle_samples', blank=True, to='sites.Site', null=True),
        ),
        migrations.AddField(
            model_name='switch',
            name='site',
            field=models.ForeignKey(related_name='waffle_switches', blank=True, to='sites.Site', null=True),
        ),
        migrations.AlterField(
            model_name='flag',
            name='name',
            field=models.CharField(help_text=b'The human/computer readable name.', max_length=100),
        ),
        migrations.AlterField(
            model_name='sample',
            name='name',
            field=models.CharField(help_text=b'The human/computer readable name.', max_length=100),
        ),
        migrations.AlterField(
            model_name='switch',
            name='name',
            field=models.CharField(help_text=b'The human/computer readable name.', max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='flag',
            unique_together=set([('name', 'site')]),
        ),
        migrations.AlterUniqueTogether(
            name='sample',
            unique_together=set([('name', 'site')]),
        ),
        migrations.AlterUniqueTogether(
            name='switch',
            unique_together=set([('name', 'site')]),
        ),
    ]
