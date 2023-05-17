from django import template

register = template.Library()

@register.filter
def nostr_short(npub):
    first_eight = npub[:8]
    last_eight = npub[-8:]
    return f"{first_eight}:{last_eight}"

@register.filter
def pretty_score(score):
    return f"{score:,}"