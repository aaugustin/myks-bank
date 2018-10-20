import re

from django.db import models
from django.utils.functional import cached_property


class Category(models.Model):
    name = models.CharField(max_length=40, unique=True, verbose_name="nom")
    order = models.SmallIntegerField(verbose_name="ordre")

    class Meta(object):
        ordering = ("name",)
        verbose_name = "catégorie"
        verbose_name_plural = "catégories"

    def __str__(self):
        return self.name


class Line(models.Model):

    BANK_CHOICES = [("CA", "Crédit Agricole"), ("LCL", "Crédit Lyonnais")]

    label = models.CharField(max_length=100, verbose_name="libellé")
    date = models.DateField(verbose_name="date de valeur")
    amount = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name="crédit ou débit"
    )

    bank = models.CharField(max_length=20, choices=BANK_CHOICES, verbose_name="banque")

    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="catégorie",
    )

    class Meta(object):
        verbose_name = "ligne"
        verbose_name_plural = "lignes"

    def __str__(self):
        return self.label

    def categorize(self, rules=None):
        if rules is None:
            rules = Rule.objects.filter(bank=self.bank)
        for rule in rules:
            if rule.compiled_re.fullmatch(self.label):
                self.category = rule.category
                break


class Rule(models.Model):

    BANK_CHOICES = Line.BANK_CHOICES

    pattern = models.CharField(max_length=1000, verbose_name="expression régulière")

    bank = models.CharField(max_length=20, choices=BANK_CHOICES, verbose_name="banque")

    category = models.ForeignKey(
        to=Category, on_delete=models.CASCADE, verbose_name="catégorie"
    )

    class Meta(object):
        verbose_name = "règle"
        verbose_name_plural = "règles"

    def __str__(self):
        return self.pattern

    @cached_property
    def re(self):
        return self.pattern.replace("--", r"[0-9]{2}")

    @cached_property
    def compiled_re(self):
        return re.compile(self.re)
