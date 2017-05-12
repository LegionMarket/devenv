# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-04 20:21
from __future__ import unicode_literals

from django.db import migrations, models
import markdownx.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('markdownx_field1', markdownx.models.MarkdownxField()),
                ('markdownx_field2', markdownx.models.MarkdownxField()),
                ('textfield1', models.TextField()),
                ('textfield2', models.TextField()),
            ],
        ),
    ]
