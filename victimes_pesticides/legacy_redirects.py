"""Repo-managed legacy redirects.

Add old URLs from the previous site here as they are discovered. Paths should
start and end with a slash. Query strings are preserved automatically.
"""

import re

from django.urls import re_path
from django.views.generic.base import RedirectView


LEGACY_REDIRECTS = {
    # Confirmed old URLs found in web search results. Add newly discovered legacy
    # URLs here only after verifying that the old path existed or is producing
    # 404s, and that the destination contains the matching current content.
    "/mission/": "/a-propos/",
    "/presse/action-qc/": "/actualites/action-qc/",
    "/presse/memoire-arla/": "/actualites/memoire-arla/",
    "/presse/petition-glyphosate/": "/actualites/petition-glyphosate/",
    "/presse/plan-agriculture-durable/": "/actualites/plan-agriculture-durable/",
    "/presse/premiere_reconnaissance/": "/actualites/premiere_reconnaissance/",
    "/presse/rapport-sondage-2025/": "/actualites/rapport-sondage-2025/",
    "/presse/reaction-annonce/": "/actualites/reaction-annonce/",
    "/presse/reconnaissance-parkinson/": "/actualites/reconnaissance-parkinson/",
    "/presse/reconnaissanceparkinson/": "/actualites/reconnaissanceparkinson/",
    "/presse/tournee2022/": "/actualites/tournee2022/",
}


def _legacy_redirect_regex(old_path):
    """Return a regex that matches the old path with or without trailing slash."""
    route = old_path.strip("/")
    if not route:
        return r"^$"
    return rf"^{re.escape(route)}/?$"


def legacy_redirect_urlpatterns():
    """Build exact redirect URL patterns from LEGACY_REDIRECTS."""
    return [
        re_path(
            _legacy_redirect_regex(old_path),
            RedirectView.as_view(
                url=new_path,
                permanent=True,
                query_string=True,
            ),
            name=f"legacy_redirect_{index}",
        )
        for index, (old_path, new_path) in enumerate(LEGACY_REDIRECTS.items())
    ]
