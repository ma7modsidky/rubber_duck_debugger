from django import template
from django.template.defaultfilters import stringfilter
import markdown as md

register = template.Library()

@register.filter
@stringfilter
def markdown(value):
    # 'extra' includes fenced code blocks, tables, and more
    return md.markdown(value, extensions=['fenced_code', 'codehilite'])