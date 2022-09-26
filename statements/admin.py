import datetime

from django.urls import path, re_path
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.template.loader import get_template
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Category, Line, Rule
from .views import average_chart, history_chart, summary


def edit(obj):
    return "Modifier"


edit.short_description = "Modifier"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "order", edit]
    list_display_links = [edit]
    list_editable = ["name", "order"]
    ordering = ["order"]
    search_fields = ["name"]


admin.site.register(Category, CategoryAdmin)


class LineChangeList(ChangeList):
    def get_results(self, request):
        super().get_results(request)

        # Annotate queryset with categories defined by rules.
        rules_cache = {}
        for line in self.result_list:
            try:
                rules = rules_cache[line.bank]
            except KeyError:
                rules = Rule.objects.filter(bank=line.bank)
                rules_cache[line.bank] = rules
            line.predicted_category = line.predict_category(rules)


class LineAdmin(admin.ModelAdmin):
    autocomplete_fields = ["category"]
    date_hierarchy = "date"
    fields = ["label", "date", "amount", "bank", "category", "predicted_category"]
    list_display = ["label", "date", "amount", "bank", "category", "match_rules"]
    list_editable = ["category"]
    list_filter = ["category", "bank", "date"]
    ordering = ["-date", "-id"]
    readonly_fields = ["predicted_category"]
    search_fields = ["label"]

    def get_changelist(self, request, **kwargs):
        return LineChangeList

    def get_search_results(self, request, queryset, search_term):
        return queryset.filter(label__iregex=search_term), False

    def get_urls(self):
        return [
            path(r"summary/", summary, name="statement-summary"),
            re_path(
                r"^average_chart/(month|year)/$",
                average_chart,
                name="statement-average-chart",
            ),
           re_path(
                r"^history_chart/(credits|debits)/$",
                history_chart,
                name="statement-history-chart",
            ),
        ] + super(LineAdmin, self).get_urls()

    def match_rules(self, obj):
        if obj.predicted_category is None:
            result = "unknown"
        elif obj.category == obj.predicted_category:
            result = "yes"
        else:
            result = "no"
        return format_html('<img src="{}">', static(f"admin/img/icon-{result}.svg"))

    match_rules.short_description = "Conforme"

    def predicted_category(self, obj):
        return obj.predict_category() or "-"

    predicted_category.short_description = "Catégorie prédite"


admin.site.register(Line, LineAdmin)


class RuleAdmin(admin.ModelAdmin):
    autocomplete_fields = ["category"]
    fields = ["pattern", "bank", "category", "last_matching_lines"]
    list_display = ["pattern", "bank", "category", edit]
    list_display_links = [edit]
    list_editable = ["pattern", "bank", "category"]
    list_filter = ["category", "bank"]
    ordering = ["pattern"]
    readonly_fields = ["last_matching_lines"]
    search_fields = ["pattern"]

    def last_matching_lines(self, obj):
        if obj.id is None:
            return "-"
        since = datetime.date.today() - datetime.timedelta(days=365)
        # label__regex does a match, not a fullmatch, so its behavior
        # may differ slightly from predict_category.
        lines = Line.objects.filter(label__regex=obj.re, date__gte=since)
        template = get_template("statements/rule_lines.html")
        context = {"rule": obj, "lines": lines.order_by("-date")}
        return mark_safe(template.render(context))

    last_matching_lines.short_description = "Lignes récentes"


admin.site.register(Rule, RuleAdmin)
