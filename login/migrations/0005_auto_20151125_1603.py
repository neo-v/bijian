# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20151121_1751'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('provence', models.CharField(help_text='provence information about your child class', max_length=50, verbose_name='provence', blank=True)),
                ('city', models.CharField(help_text='city information about your child class', max_length=50, verbose_name='city', blank=True)),
                ('school', models.CharField(help_text='school information about your child class', max_length=50, verbose_name='school', blank=True)),
                ('grade', models.CharField(help_text='grade information about your child class', max_length=50, verbose_name='grade', blank=True)),
                ('classes', models.CharField(help_text='class information', max_length=50, verbose_name='class', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course', models.CharField(help_text='school courses', max_length=50, verbose_name='course')),
                ('intro', models.CharField(max_length=256, verbose_name='introduction', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('avatar', models.CharField(max_length=256, verbose_name='avatar', blank=True)),
                ('intro', models.CharField(max_length=256, verbose_name='introduce', blank=True)),
                ('real_name', models.CharField(max_length=30, verbose_name='real_name', blank=True)),
                ('contact_phone', models.CharField(help_text='Required numbers only.', max_length=30, verbose_name='contact_phone', blank=True)),
                ('record_count', models.PositiveIntegerField(default=0, verbose_name='record')),
                ('question_count', models.PositiveIntegerField(default=0, verbose_name='question')),
                ('answer_count', models.PositiveIntegerField(default=0, verbose_name='answer')),
                ('forward_count', models.PositiveIntegerField(default=0, verbose_name='forward')),
                ('dig_count', models.PositiveIntegerField(default=0, verbose_name='dig')),
                ('bury_count', models.PositiveIntegerField(default=0, verbose_name='bury')),
                ('visit_count', models.PositiveIntegerField(default=0, verbose_name='visited')),
                ('follower_count', models.PositiveIntegerField(default=0, verbose_name='follower')),
                ('followee_count', models.PositiveIntegerField(default=0, verbose_name='followee')),
                ('msg_count', models.PositiveIntegerField(default=0, verbose_name='message')),
                ('review_count', models.PositiveIntegerField(default=0, verbose_name='review')),
                ('is_identify', models.BooleanField(default=False, verbose_name='identify')),
                ('identity', models.CharField(max_length=256, verbose_name='identity', blank=True)),
                ('is_online', models.BooleanField(default=False, verbose_name='online')),
            ],
        ),
        migrations.CreateModel(
            name='ParentDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('avatar', models.CharField(max_length=256, verbose_name='avatar', blank=True)),
                ('intro', models.CharField(max_length=256, verbose_name='introduce', blank=True)),
                ('child_name', models.CharField(max_length=30, verbose_name='child_name', blank=True)),
                ('real_name', models.CharField(max_length=30, verbose_name='real_name', blank=True)),
                ('nick_name', models.CharField(max_length=30, verbose_name='nick_name', blank=True)),
                ('record_count', models.PositiveIntegerField(default=0, verbose_name='record')),
                ('question_count', models.PositiveIntegerField(default=0, verbose_name='question')),
                ('answer_count', models.PositiveIntegerField(default=0, verbose_name='answer')),
                ('forward_count', models.PositiveIntegerField(default=0, verbose_name='forward')),
                ('dig_count', models.PositiveIntegerField(default=0, verbose_name='dig')),
                ('bury_count', models.PositiveIntegerField(default=0, verbose_name='bury')),
                ('visit_count', models.PositiveIntegerField(default=0, verbose_name='visited')),
                ('follower_count', models.PositiveIntegerField(default=0, verbose_name='follower')),
                ('followee_count', models.PositiveIntegerField(default=0, verbose_name='followee')),
                ('msg_count', models.PositiveIntegerField(default=0, verbose_name='message')),
                ('review_count', models.PositiveIntegerField(default=0, verbose_name='review')),
                ('is_online', models.BooleanField(default=False, verbose_name='online')),
                ('class_id', models.ForeignKey(related_name='parent_in', to='login.ClassInformation')),
            ],
        ),
        migrations.CreateModel(
            name='SchoolDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('avatar', models.CharField(max_length=256, verbose_name='avatar', blank=True)),
                ('intro', models.CharField(max_length=256, verbose_name='introduce', blank=True)),
                ('courses', models.CharField(max_length=256, verbose_name='courses', blank=True)),
                ('school_name', models.CharField(max_length=30, verbose_name='real_name', blank=True)),
                ('contact_phone', models.CharField(help_text='Required numbers only.', max_length=30, verbose_name='contact_phone', blank=True)),
                ('record_count', models.PositiveIntegerField(default=0, verbose_name='record')),
                ('question_count', models.PositiveIntegerField(default=0, verbose_name='question')),
                ('answer_count', models.PositiveIntegerField(default=0, verbose_name='answer')),
                ('forward_count', models.PositiveIntegerField(default=0, verbose_name='forward')),
                ('dig_count', models.PositiveIntegerField(default=0, verbose_name='dig')),
                ('bury_count', models.PositiveIntegerField(default=0, verbose_name='bury')),
                ('visit_count', models.PositiveIntegerField(default=0, verbose_name='visited')),
                ('follower_count', models.PositiveIntegerField(default=0, verbose_name='follower')),
                ('followee_count', models.PositiveIntegerField(default=0, verbose_name='followee')),
                ('msg_count', models.PositiveIntegerField(default=0, verbose_name='message')),
                ('review_count', models.PositiveIntegerField(default=0, verbose_name='review')),
                ('is_identify', models.BooleanField(default=False, verbose_name='identify')),
                ('identity', models.CharField(max_length=256, verbose_name='identity', blank=True)),
                ('is_online', models.BooleanField(default=False, verbose_name='online')),
            ],
        ),
        migrations.CreateModel(
            name='TeacherDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('avatar', models.CharField(max_length=256, verbose_name='avatar', blank=True)),
                ('intro', models.CharField(max_length=256, verbose_name='introduce', blank=True)),
                ('real_name', models.CharField(max_length=30, verbose_name='real_name', blank=True)),
                ('nick_name', models.CharField(max_length=30, verbose_name='nick_name', blank=True)),
                ('contact_phone', models.CharField(help_text='Required numbers only.', max_length=30, verbose_name='contact_phone', blank=True)),
                ('record_count', models.PositiveIntegerField(default=0, verbose_name='record')),
                ('question_count', models.PositiveIntegerField(default=0, verbose_name='question')),
                ('answer_count', models.PositiveIntegerField(default=0, verbose_name='answer')),
                ('forward_count', models.PositiveIntegerField(default=0, verbose_name='forward')),
                ('dig_count', models.PositiveIntegerField(default=0, verbose_name='dig')),
                ('bury_count', models.PositiveIntegerField(default=0, verbose_name='bury')),
                ('visit_count', models.PositiveIntegerField(default=0, verbose_name='visited')),
                ('follower_count', models.PositiveIntegerField(default=0, verbose_name='follower')),
                ('followee_count', models.PositiveIntegerField(default=0, verbose_name='followee')),
                ('msg_count', models.PositiveIntegerField(default=0, verbose_name='message')),
                ('review_count', models.PositiveIntegerField(default=0, verbose_name='review')),
                ('is_online', models.BooleanField(default=False, verbose_name='online')),
                ('is_identify', models.BooleanField(default=False, verbose_name='identify')),
                ('is_adviser', models.BooleanField(default=False, verbose_name='class adviser')),
                ('class_id', models.ForeignKey(related_name='teacher_in', to='login.ClassInformation')),
                ('course', models.ForeignKey(related_name='course_of', to='login.CourseInformation')),
            ],
        ),
        migrations.DeleteModel(
            name='UserDetail',
        ),
        migrations.AddField(
            model_name='localuser',
            name='social_id',
            field=models.CharField(max_length=30, verbose_name='social_id', blank=True),
        ),
        migrations.AddField(
            model_name='localuser',
            name='type',
            field=models.CharField(default='PR', max_length=30, verbose_name='type', blank=True, choices=[('TC', 'teacher'), ('SC', 'school'), ('OG', 'organization'), ('PR', 'parent')]),
        ),
        migrations.AddField(
            model_name='teacherdetail',
            name='user',
            field=models.ForeignKey(related_name='teacher_of', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='schooldetail',
            name='user',
            field=models.OneToOneField(related_name='school_of', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='parentdetail',
            name='user',
            field=models.OneToOneField(related_name='parent_of', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='organizationdetail',
            name='user',
            field=models.OneToOneField(related_name='organization_of', to=settings.AUTH_USER_MODEL),
        ),
    ]
