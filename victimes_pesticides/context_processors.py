"""
Context processors for making data available to all templates.
"""
from wagtail.models import Page, Site


def navigation(request):
    """
    Add navigation menu items to the context.
    Gets all pages marked with 'show_in_menus' from the site root.
    """
    site = Site.find_for_request(request)
    if site:
        menuitems = site.root_page.get_children().live().in_menu()
    else:
        menuitems = Page.objects.none()

    return {
        'menuitems': menuitems,
    }
