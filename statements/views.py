import datetime

import pygal
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render

from .models import Category


FIRST_YEAR = 2013  # first year with complete records


def summary(request):
    cursor = connection.cursor()
    sql = """
    SELECT  strftime('%Y%m', date) AS month, sum(amount)
      FROM  statements_line
     WHERE  amount > 0
  GROUP BY  month
"""
    credits = dict(cursor.execute(sql).fetchall())
    sql = sql.replace("amount > 0", "amount < 0")
    debits = dict(cursor.execute(sql).fetchall())
    months = sorted(set(credits.keys()) | set(debits.keys()))
    total, totals = 0, {}
    for month in months:
        total += credits.get(month, 0) + debits.get(month, 0)
        totals[month] = total
    data = [
        [
            datetime.date(int(month[:4]), int(month[4:]), 1),
            credits.get(month, 0),
            debits.get(month, 0),
            totals.get(month, 0),
        ]
        for month in reversed(months)
    ]
    context = {"title": "Résumé", "data": data}
    return render(request, "statements/summary.html", context)


def average_chart(request, period):
    assert period in ("month", "year")
    show_year = period == "year"

    this_month = datetime.date.today().replace(day=1)
    if show_year:
        since = this_month.replace(year=this_month.year - 1)
    else:
        if this_month.month == 1:
            since = this_month.replace(year=this_month.year - 1, month=12)
        else:
            since = this_month.replace(month=this_month.month - 1)
    until = this_month - datetime.timedelta(days=1)

    cursor = connection.cursor()
    sql = """
     SELECT category_id, -sum(amount)
      FROM  statements_line
     WHERE  amount < 0 AND amount > -3000 AND date BETWEEN %s AND %s
  GROUP BY  category_id
"""
    amounts = dict(cursor.execute(sql, [since, until]).fetchall())

    categories = Category.objects.exclude(order__lt=0).order_by("order")

    chart = pygal.Pie(
        width=600,
        height=400,
        fill=True,
        include_x_axis=True,
        style=pygal.style.DefaultStyle,
    )
    for cat_name, cat_id in categories.values_list("name", "id"):
        chart.add(cat_name, amounts.get(cat_id, 0))
    if None in amounts:
        chart.add("Inconnu", amounts.get(None, 0))
    return HttpResponse(chart.render(), content_type="image/svg+xml")


def last_12m_chart(request):
    today = datetime.date.today()
    year, month = today.year, today.month
    months = []
    for _ in range(12):
        if month == 1:
            month, year = 12, year - 1
        else:
            month = month - 1
        months.append(datetime.date(year, month, 1))
    months = list(reversed(months))

    cursor = connection.cursor()
    sql = """
    SELECT  strftime('%Y%m', date) AS month, category_id, sum(-amount)
      FROM  statements_line
     WHERE  amount > -3000 AND amount < 3000
  GROUP BY  month, category_id
"""

    amounts = {}
    cat_ids = set()
    for month, cat_id, amount in cursor.execute(sql).fetchall():
        amounts[(month, cat_id)] = amount
        cat_ids.add(cat_id)

    categories = (
        Category.objects.filter(id__in=cat_ids).exclude(order__lt=0).order_by("order")
    )

    chart = pygal.StackedLine(
        width=1200,
        height=800,
        fill=True,
        interpolate='cubic',
        include_x_axis=True,
        style=pygal.style.DefaultStyle,
    )
    chart.x_labels = [month.strftime("%m/%y") for month in months]
    for cat_name, cat_id in categories.values_list("name", "id"):
        chart.add(
            cat_name,
            [amounts.get((month.strftime("%Y%m"), cat_id), 0) for month in months],
        )
    if None in cat_ids:
        chart.add(
            "Inconnu",
            [amounts.get((month.strftime("%Y%m"), None), 0) for month in months],
        )
    return HttpResponse(chart.render(), content_type="image/svg+xml")


def history_chart(request):
    today = datetime.date.today()
    years = [datetime.date(year, 1, 1) for year in range(FIRST_YEAR, today.year)]

    cursor = connection.cursor()
    sql = """
    SELECT  strftime('%Y', date) AS year, category_id, sum(-amount)
      FROM  statements_line
     WHERE  amount > -3000 AND amount < 3000
  GROUP BY  year, category_id
"""

    amounts = {}
    cat_ids = set()
    for year, cat_id, amount in cursor.execute(sql).fetchall():
        amounts[(year, cat_id)] = amount
        cat_ids.add(cat_id)

    categories = (
        Category.objects.filter(id__in=cat_ids).exclude(order__lt=0).order_by("order")
    )

    chart = pygal.StackedLine(
        width=1200,
        height=800,
        fill=True,
        interpolate='cubic',
        include_x_axis=True,
        style=pygal.style.DefaultStyle,
    )
    chart.x_labels = [year.strftime("%y") for year in years]
    for cat_name, cat_id in categories.values_list("name", "id"):
        chart.add(
            cat_name,
            [amounts.get((year.strftime("%Y"), cat_id), 0) for year in years],
        )
    if None in cat_ids:
        chart.add(
            "Inconnu",
            [amounts.get((year.strftime("%Y"), None), 0) for year in years],
        )
    return HttpResponse(chart.render(), content_type="image/svg+xml")
