"""Template tags for displaying actualites (news articles)"""
import hashlib
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


@register.filter
def color_from_string(value):
    """
    Generate a consistent color gradient based on a string.
    Same string will always generate the same color.

    Args:
        value: String to generate color from (typically article title)

    Returns:
        Tailwind gradient classes
    """
    # Predefined color combinations that work well together
    color_schemes = [
        'from-green-100 to-green-200',
        'from-blue-100 to-blue-200',
        'from-purple-100 to-purple-200',
        'from-orange-100 to-orange-200',
        'from-teal-100 to-teal-200',
        'from-indigo-100 to-indigo-200',
        'from-pink-100 to-pink-200',
        'from-cyan-100 to-cyan-200',
        'from-emerald-100 to-emerald-200',
        'from-rose-100 to-rose-200',
    ]

    # Generate hash from string and convert to index
    hash_value = int(hashlib.md5(str(value).encode()).hexdigest(), 16)
    index = hash_value % len(color_schemes)

    return color_schemes[index]
