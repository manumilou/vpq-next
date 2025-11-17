"""Template tags for displaying actualites (news articles)"""
from django import template
from actualites.models import ActualitePage

register = template.Library()


@register.simple_tag
def get_latest_actualites(count=3):
    """
    Get the latest published news articles.

    Args:
        count: Number of articles to return (default: 3)

    Returns:
        QuerySet of ActualitePage objects
    """
    return ActualitePage.objects.live().public().order_by('-date_publication')[:count]


@register.simple_tag
def get_featured_actualites(count=3):
    """
    Get featured news articles.

    Args:
        count: Number of articles to return (default: 3)

    Returns:
        QuerySet of ActualitePage objects marked as featured
    """
    return ActualitePage.objects.live().public().filter(
        mise_en_vedette=True
    ).order_by('-date_publication')[:count]
