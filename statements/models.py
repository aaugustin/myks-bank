# coding: utf-8

from __future__ import unicode_literals

import re

from django.db import models
from django.utils.functional import cached_property


class Category(models.Model):
    name = models.CharField(max_length=40, unique=True, verbose_name="nom")
    order = models.SmallIntegerField(verbose_name="ordre")

    class Meta(object):
        ordering = 'name',
        verbose_name = "catégorie"
        verbose_name_plural = "catégories"

    def __unicode__(self):
        return self.name


class Line(models.Model):

    BANK_CHOICES = [
        ('CA', "Crédit Agricole"),
        ('LCL', "Crédit Lyonnais"),
    ]

    label = models.CharField(max_length=100, verbose_name="libellé")
    date = models.DateField(verbose_name="date de valeur")
    amount = models.DecimalField(max_digits=9, decimal_places=2,
                                 verbose_name="crédit ou débit")

    bank = models.CharField(max_length=20, choices=BANK_CHOICES,
                            verbose_name="banque")

    category = models.ForeignKey(Category, blank=True, null=True,
                                 verbose_name="catégorie")

    class Meta(object):
        verbose_name = "ligne"
        verbose_name_plural = "lignes"

    def __unicode__(self):
        return self.label

    def categorize(self, rules=None):
        if rules is None:
            rules = Rule.objects.all()
        for rule in rules:
            if rule.compiled_re.match(self.label):
                self.category = rule.category
                break


class Rule(models.Model):
    pattern = models.CharField(max_length=1000,
                               verbose_name="expression régulière")
    category = models.ForeignKey(Category, verbose_name="catégorie")

    class Meta(object):
        verbose_name = "règle"
        verbose_name_plural = "règles"

    def __unicode__(self):
        return self.pattern

    @cached_property
    def re(self):
        return '^%s$' % self.pattern.replace('--/--/--',
                                             r'\d{2}/\d{2}/\d{2}')

    @cached_property
    def compiled_re(self):
        return re.compile(self.re)
