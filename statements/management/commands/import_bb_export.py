import csv
import datetime
import decimal
import sys

from django.core.management import base
from django.db import transaction

from ...models import Category, Line, Rule


class Command(base.BaseCommand):
    help = "Read CSV export from stdin and process it."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Do not save statement lines to the database.",
        )

    @transaction.atomic
    def handle(self, **options):
        assert sys.stdin.read(1) == "\ufeff"  # remove BOM
        rows = csv.DictReader(sys.stdin, delimiter=";")
        verbosity = int(options["verbosity"])
        rules = Rule.objects.filter(bank="BB")

        for row in reversed(list(rows)):
            line = Line(
                label=row["label"],
                date=datetime.date.fromisoformat(row["dateVal"]),
                amount=decimal.Decimal(row["amount"].replace(",", ".").replace(" ", "")),
                balance=decimal.Decimal(row["accountbalance"]),
                bank="BB",
            )

            line.category = line.predict_category(rules)

            if verbosity >= 1:
                print(
                    ("✅" if line.category else "❌") +
                    f" {line.date}  {line.amount:+8.2f}  {line.label:40}"
                    f" -> {line.category or '???'}"
                )

            if not options["dry_run"]:
                line.save()
