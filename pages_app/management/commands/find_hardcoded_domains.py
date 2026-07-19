"""Find hardcoded domain references in database-backed content.

Useful before switching the public domain: scans text/URL/JSON fields across
installed Django models, including Wagtail StreamField/RichText content and
revisions, and reports any references to temporary domains.
"""

from __future__ import annotations

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import models


DEFAULT_DOMAINS = [
    "vpq.pythonanywhere.com",
    "victimespesticidesquebec.pythonanywhere.com",
]


class Command(BaseCommand):
    help = "Find hardcoded domain references in database text/URL/JSON fields."

    def add_arguments(self, parser):
        parser.add_argument(
            "--domain",
            action="append",
            dest="domains",
            help=(
                "Domain/string to search for. Can be passed multiple times. "
                f"Defaults to: {', '.join(DEFAULT_DOMAINS)}"
            ),
        )
        parser.add_argument(
            "--context",
            type=int,
            default=90,
            help="Characters of context to print around each match. Default: 90",
        )
        parser.add_argument(
            "--fail-on-match",
            action="store_true",
            help="Exit with status 1 if any matches are found.",
        )

    def handle(self, *args, **options):
        domains = options["domains"] or DEFAULT_DOMAINS
        context = options["context"]
        total_matches = 0
        scanned_fields = 0

        self.stdout.write("Searching database content for hardcoded domains:")
        for domain in domains:
            self.stdout.write(f"  - {domain}")
        self.stdout.write("")

        for model in apps.get_models():
            fields = [field for field in model._meta.fields if self._is_searchable_field(field)]
            if not fields:
                continue

            pk_name = model._meta.pk.name
            model_label = model._meta.label

            for field in fields:
                scanned_fields += 1
                try:
                    rows = model._default_manager.values_list(pk_name, field.name).iterator(chunk_size=500)
                    for pk, value in rows:
                        if value in (None, ""):
                            continue

                        text = str(value)
                        matched_domains = [domain for domain in domains if domain in text]
                        if not matched_domains:
                            continue

                        for domain in matched_domains:
                            total_matches += text.count(domain)
                            snippet = self._snippet(text, domain, context)
                            self.stdout.write(self.style.WARNING(f"{model_label} pk={pk} field={field.name}"))
                            self.stdout.write(f"  matched: {domain}")
                            self.stdout.write(f"  ...{snippet}...")
                            self.stdout.write("")
                except Exception as exc:  # Keep scanning even if one model/field is unusual.
                    self.stdout.write(self.style.NOTICE(f"Skipped {model_label}.{field.name}: {exc}"))

        if total_matches:
            self.stdout.write(self.style.ERROR(f"Found {total_matches} hardcoded domain reference(s)."))
            if options["fail_on_match"]:
                raise SystemExit(1)
        else:
            self.stdout.write(self.style.SUCCESS("No hardcoded domain references found."))

        self.stdout.write(f"Scanned {scanned_fields} searchable field(s).")

    @staticmethod
    def _is_searchable_field(field):
        if not getattr(field, "concrete", False):
            return False

        if isinstance(field, (models.CharField, models.TextField, models.URLField, models.EmailField, models.JSONField)):
            return True

        # Covers custom fields such as Wagtail StreamField if they do not inherit
        # directly from Django's JSON/Text field classes in a future version.
        return field.get_internal_type() in {
            "CharField",
            "TextField",
            "URLField",
            "EmailField",
            "JSONField",
            "StreamField",
        }

    @staticmethod
    def _snippet(text, needle, context):
        index = text.find(needle)
        start = max(index - context, 0)
        end = min(index + len(needle) + context, len(text))
        return " ".join(text[start:end].split())
