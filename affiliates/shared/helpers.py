import json

from jingo import register

from affiliates.shared.utils import absolutify as utils_absolutify


@register.function
def absolutify(*args, **kwargs):
    """Return the given url with an added domain and protocol."""
    return utils_absolutify(*args, **kwargs)


@register.filter
def jsonencode(data):
    return json.dumps(data)
