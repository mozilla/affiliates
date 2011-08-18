from jingo import register


@register.filter
def wizard_active(step, current):
    """
    Return the proper classname for the step div in the badge wizard.

    The current step needs a 'selected' class while the following step needs a
    'next-selected' class to color the tip of the arrow properly.
    """
    if current == step:
        return 'selected'
    elif (current + 1) == step:
        return 'next-selected'
