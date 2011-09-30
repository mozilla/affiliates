# Sizes for banners/fixtures/banners.json
sizes = ['120x240', '120x240', '120x240', '300x250', '300x250']


@property
def mock_size(self):
    """Mock method to prevent tests from trying to open nonexistent images."""
    return '%s pixels' % sizes[self.pk - 1]
