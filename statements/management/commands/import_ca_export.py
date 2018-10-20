import codecs
import csv
import datetime
import decimal
import sys

from django.core.management import base
from django.db import transaction

from ...models import Category, Line, Rule


CATEGORY_MAPPING = {
    "Alimentation": ["Alimentation"],
    "Cadeaux": ["Cadeaux", "Dons"],
    "Enfants": ["Cantine", "Enfants"],
    "Équipement": ["Ameublement/équipement", "Jardin"],
    "Frais bancaires": ["Frais bancaires"],
    "Logement": ["Travaux"],
    "Loisirs": [
        "Hôtels",
        "Loisirs",
        "Restaurant",
        "Sorties",
        "Sport",
        "Transports",
        "Vacances",
    ],
    "Retraits": ["Retrait d'argent"],
    "Revenu foncier": ["Revenu foncier"],
    "Santé": ["Pharmacie", "Santé/Bien être"],
    "Voiture": ["Assurance auto", "Essence", "Parking", "Péages", "Véhicule"],
    "Vêtements": ["Chaussures", "Habillement"],
    "Virements": ["", "Prêts"],
}


class Command(base.BaseCommand):
    help = "Read CSV export from stdin and process it."

    @transaction.atomic
    def handle(self, **options):
        rows = csv.reader(
            codecs.getreader("windows-1252")(sys.stdin.buffer), delimiter=";"
        )
        assert next(rows) == [
            "Libellé",
            "Date",
            "Montant",
            "Nom du compte",
            "N° du compte",
            "Catégorie",
            "Mode de paiement",
        ]

        verbosity = int(options["verbosity"])
        rules = Rule.objects.filter(bank="CA")
        category_mapping = {
            source: Category.objects.get(name=target)
            for target, sources in CATEGORY_MAPPING.items()
            for source in sources
        }

        for (
            label,
            date,
            amount,
            account_name,
            account_number,
            category,
            payment_means,
        ) in rows:
            date = datetime.date(*reversed(list(map(int, date.split("/")))))
            amount = decimal.Decimal(amount.replace(",", "."))
            line = Line(label=label, date=date, amount=amount, bank="CA")

            line.categorize(rules=rules)
            if line.category is None:
                line.category = category_mapping.get(category)

            if verbosity >= 1:
                print(
                    f"{date}  {amount:+8.2f}  {label:32}  {category:24}"
                    f" -> {line.category or '???'}"
                )

            line.save()
