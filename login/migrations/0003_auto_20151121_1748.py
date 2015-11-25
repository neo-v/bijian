# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20151121_0243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address', error_messages={'unique': 'A user with that email already exists.'}),
        ),
    ]
