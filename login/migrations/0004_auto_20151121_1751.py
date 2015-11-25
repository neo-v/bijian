# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_auto_20151121_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address', error_messages={'unique': 'A email with that email already exists.'}),
        ),
        migrations.AlterField(
            model_name='localuser',
            name='username',
            field=models.CharField(validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], error_messages={'unique': 'A username with that username already exists.'}, max_length=30, blank=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', verbose_name='username'),
        ),
    ]
