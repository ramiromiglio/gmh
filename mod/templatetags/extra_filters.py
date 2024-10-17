from django import template

register = template.Library()

@register.filter
def pretty_size(nbytes):
    if isinstance(nbytes, int):
        if nbytes >= 1_000_000:
            return "{:.1f} MB".format(nbytes / 1_000_000)
        if nbytes >= 1_000:
            return "{:.1f} KB".format(nbytes / 1_000)
        return str(nbytes) + " B"
    return nbytes

@register.filter
def is_even(n):
    return n % 2 == 0