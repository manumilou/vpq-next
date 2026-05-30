"""Template tags for pages_app"""
from django import template
from django.utils.text import slugify

register = template.Library()


@register.simple_tag
def get_link_url(link_block):
    """
    Get URL from a LinkBlock.

    Args:
        link_block: A LinkBlock value (StructValue)

    Returns:
        str: The URL to use in href attribute
    """
    if not link_block:
        return '#'

    link_type = link_block.get('link_type', 'internal')

    if link_type == 'internal' and link_block.get('internal_page'):
        return link_block['internal_page'].url
    elif link_type == 'external' and link_block.get('external_url'):
        return link_block['external_url']
    elif link_type == 'anchor' and link_block.get('anchor_id'):
        return f"#{slugify(link_block['anchor_id'].lstrip('#'))}"

    return '#'
