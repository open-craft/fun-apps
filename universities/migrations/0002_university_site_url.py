# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('universities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='university',
            name='site_url',
            field=models.CharField(help_text='Link to the external site for this university.', max_length=1024, verbose_name='site url', blank=True),
        ),
    ]
