from tower import ugettext as _


COLORS = ['Blue', 'Green', 'Red', 'Orange', 'Yellow', 'White', 'Black']
LOCALIZED_COLORS = [_(color) for color in COLORS]
COLOR_CHOICES = zip(COLORS, LOCALIZED_COLORS)
