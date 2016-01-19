# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification_center', '0010_auto_20150218_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationevent',
            name='description',
            field=models.CharField(default='no descriptioN', max_length=50),
            preserve_default=False,
        ),
    ]
