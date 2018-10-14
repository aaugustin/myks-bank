import datetime

from django.contrib import admin
from django.conf.urls import url
from django.template import Context
from django.template.loader import get_template
from django.utils.safestring import mark_safe

from .models import Category, Line, Rule
from .views import summary, average_chart, history_chart


class CategoryAdmin(admin.ModelAdmin):
    list_display = 'edit', 'order', 'name',
    list_editable = 'order', 'name',
    ordering = 'order',

    def edit(self, obj):
        return "Modifier"
    edit.short_description = "Modifier"

admin.site.register(Category, CategoryAdmin)


class LineAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = 'label', 'date', 'amount', 'bank', 'category'
    list_editable = 'category',
    list_filter = 'category', 'bank', 'date'
    ordering = '-date', '-id'
    search_fields = 'label', 'category__name'

    def get_urls(self):
        return [
            url(r'^summary/$', summary,
                name='statement-summary'),
            url(r'^average_chart/(month|year)/$', average_chart,
                name='statement-average-chart'),
            url(r'^history_chart/(credits|debits)/$', history_chart,
                name='statement-history-chart'),
        ] + super(LineAdmin, self).get_urls()


admin.site.register(Line, LineAdmin)


class RuleAdmin(admin.ModelAdmin):
    fields = 'pattern', 'category', 'last_matching_lines'
    list_display = 'pattern', 'category'
    list_editable = 'category',
    list_filter = 'category',
    ordering = 'pattern', 'category'
    readonly_fields = 'last_matching_lines',
    search_fields = 'pattern',

    def last_matching_lines(self, obj):
        since = datetime.date.today() - datetime.timedelta(days=365)
        lines = Line.objects.filter(label__regex=obj.re, date__gte=since)
        template = get_template('statements/rule_lines.html')
        context = {
            'rule': obj,
            'lines': lines.order_by('-date'),
        }
        return mark_safe(template.render(context))
    last_matching_lines.short_description = "Lignes récentes"

admin.site.register(Rule, RuleAdmin)
