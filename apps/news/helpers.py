from jingo import register

from news.models import NewsItem


@register.function
def get_latest_newsitem():
    """Get the latest news item able to be shown."""
    try:
        return NewsItem.objects.filter(enabled=True).order_by('-created').get()
    except NewsItem.DoesNotExist:
        return None
