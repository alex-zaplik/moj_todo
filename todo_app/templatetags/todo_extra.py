from django import template

register = template.Library()

@register.filter
def next_elem(a_list, index):
    try:
        return a_list[int(index) + 1]
    except:
        return ''


@register.filter
def prev_elem(a_list, index):
    try:
        return a_list[int(index) - 1]
    except:
        return ''