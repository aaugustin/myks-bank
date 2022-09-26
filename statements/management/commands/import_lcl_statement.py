import collections
import datetime
import decimal
import sys

from django.core.management import base
from django.db import transaction
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage

from ...models import Line, Rule


class CustomConverter(PDFPageAggregator):

    # Horizontal coordinates of vertical lines that delimit columns.
    boundaries = [38, 70, 358, 404, 482, 560]
    boundaries = list(zip(boundaries[:-1], boundaries[1:]))

    def __init__(self, *args, **kwargs):
        laparams = LAParams(char_margin=1.2, line_margin=0.1)
        kwargs.setdefault("laparams", laparams)
        super(CustomConverter, self).__init__(*args, **kwargs)
        # Public variable holding relevant rows when processing is complete.
        self.rows = []

    def receive_layout(self, ltpage):
        """Extract data rows."""
        # Group pieces of text by vertical coordinate.
        rows = collections.defaultdict(lambda: [[] for _ in self.boundaries])
        for item in ltpage:
            if isinstance(item, LTTextBox):
                for col, (left, right) in enumerate(self.boundaries):
                    if left - 1 < item.x0 < item.x1 < right + 1:
                        rows[int(item.y0)][col].append(item.get_text().strip())
                        break
        # Merge almost aligned pieces of text.
        sorted_rows = sorted(rows.items(), reverse=True)
        for (y1, row1), (y2, row2) in zip(sorted_rows[:-1], sorted_rows[1:]):
            if y1 - y2 < 6:
                rows[y1] = [item1 + item2 for item1, item2 in zip(row1, row2)]
                del rows[y2]
        # Process relevant rows and store their data.
        for _, row in sorted(rows.items(), reverse=True):
            row = [" ".join(item) for item in row]
            if not all(row[:3]):
                continue
            if row == ["DATE", "LIBELLE", "VALEUR", "DEBIT", "CREDIT"]:
                continue
            label = row[1]
            day, month, year = map(int, row[2].split("."))
            date = datetime.date(2000 + year, month, day)
            amount = "-" + row[3] if "," in row[3] else row[4]
            amount = decimal.Decimal(amount.replace(" ", "").replace(",", "."))
            self.rows.append((label, date, amount))

    def render_image(self, name, stream):
        """Ignore images."""

    def paint_path(self, gstate, stroke, fill, evenodd, path):
        """Ignore paths."""


class Command(base.BaseCommand):
    help = "Read PDF statement from stdin and process it."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Do not save statement lines to the database.",
        )

    @transaction.atomic
    def handle(self, **options):
        # PDFMiner boilerplate. (Cool API!)
        rsrcmgr = PDFResourceManager()
        device = CustomConverter(rsrcmgr)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(sys.stdin.buffer):
            interpreter.process_page(page)
        rows = device.rows

        # Process extracted rows.
        verbosity = int(options["verbosity"])
        rules = Rule.objects.filter(bank="LCL")
        for label, date, amount in rows:
            line = Line(label=label, date=date, amount=amount, bank="LCL")

            line.category = line.predict_category(rules)

            if verbosity >= 1:
                print(
                    ("✅" if line.category else "❌") +
                    f" {date}  {amount:+8.2f}  {label:32}"
                    f" -> {line.category or '???'}"
                )

            if not options["dry_run"]:
                line.save()
