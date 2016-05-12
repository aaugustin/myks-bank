# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=40, verbose_name='nom')),
                ('order', models.SmallIntegerField(verbose_name='ordre')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'cat\xe9gorie',
                'verbose_name_plural': 'cat\xe9gories',
            },
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=100, verbose_name='libell\xe9')),
                ('date', models.DateField(verbose_name='date de valeur')),
                ('amount', models.DecimalField(verbose_name='cr\xe9dit ou d\xe9bit', max_digits=9, decimal_places=2)),
                ('category', models.ForeignKey(verbose_name='cat\xe9gorie', blank=True, to='statements.Category', null=True)),
            ],
            options={
                'verbose_name': 'ligne',
                'verbose_name_plural': 'lignes',
            },
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pattern', models.CharField(max_length=1000, verbose_name='expression r\xe9guli\xe8re')),
                ('category', models.ForeignKey(verbose_name='cat\xe9gorie', to='statements.Category')),
            ],
            options={
                'verbose_name': 'r\xe8gle',
                'verbose_name_plural': 'r\xe8gles',
            },
        ),
    ]
