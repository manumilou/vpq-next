"""
Management command to scrape full article content from the current VPQ website
and update the Wagtail database with complete, authentic content.
"""
from django.core.management.base import BaseCommand
from actualites.models import ActualitePage
import urllib.request
import urllib.error
from html.parser import HTMLParser
import html
import re


class ArticleContentParser(HTMLParser):
    """Custom HTML parser to extract article content"""

    def __init__(self):
        super().__init__()
        self.in_main_content = False
        self.in_header = False
        self.in_nav = False
        self.in_footer = False
        self.in_paragraph = False
        self.in_heading = False
        self.in_list = False
        self.in_list_item = False
        self.in_strong = False
        self.in_em = False
        self.in_link = False

        self.current_tag = None
        self.current_heading_level = None
        self.link_href = None

        self.content_blocks = []
        self.current_text = ""

    def handle_starttag(self, tag, attrs):
        """Handle opening tags"""
        attrs_dict = dict(attrs)

        # Skip navigation, header, footer
        if tag in ['nav', 'header', 'footer']:
            if tag == 'nav':
                self.in_nav = True
            elif tag == 'header':
                self.in_header = True
            elif tag == 'footer':
                self.in_footer = True
            return

        # Skip if in excluded sections
        if self.in_nav or self.in_header or self.in_footer:
            return

        # Detect main content area
        if tag in ['section', 'article', 'main']:
            if 'class' in attrs_dict:
                # Look for content-related classes
                class_names = attrs_dict['class'].lower()
                if any(keyword in class_names for keyword in ['ressources', 'content', 'article', 'post']):
                    self.in_main_content = True

        # Only process content tags if in main content
        if not self.in_main_content:
            return

        if tag == 'p':
            self.in_paragraph = True
            self.current_text = ""
        elif tag in ['h1', 'h2', 'h3', 'h4']:
            # Skip h1 as it's usually the page title
            if tag != 'h1':
                self.in_heading = True
                self.current_heading_level = tag
                self.current_text = ""
        elif tag == 'ul':
            self.in_list = True
            self.current_text = "<ul>"
        elif tag == 'ol':
            self.in_list = True
            self.current_text = "<ol>"
        elif tag == 'li' and self.in_list:
            self.in_list_item = True
            self.current_text += "<li>"
        elif tag == 'strong' or tag == 'b':
            self.in_strong = True
        elif tag == 'em' or tag == 'i':
            self.in_em = True
        elif tag == 'a':
            self.in_link = True
            self.link_href = attrs_dict.get('href', '#')

    def handle_endtag(self, tag):
        """Handle closing tags"""
        # Reset excluded sections
        if tag == 'nav':
            self.in_nav = False
            return
        elif tag == 'header':
            self.in_header = False
            return
        elif tag == 'footer':
            self.in_footer = False
            return

        if self.in_nav or self.in_header or self.in_footer:
            return

        if tag == 'p' and self.in_paragraph:
            self.in_paragraph = False
            if self.current_text.strip():
                self.content_blocks.append(('paragraph', self.current_text.strip()))
            self.current_text = ""
        elif tag in ['h2', 'h3', 'h4'] and self.in_heading:
            self.in_heading = False
            if self.current_text.strip():
                self.content_blocks.append(('heading', self.current_text.strip()))
            self.current_text = ""
        elif tag == 'ul' and self.in_list:
            self.in_list = False
            self.current_text += "</ul>"
            if self.current_text.strip():
                self.content_blocks.append(('list', self.current_text.strip()))
            self.current_text = ""
        elif tag == 'ol' and self.in_list:
            self.in_list = False
            self.current_text += "</ol>"
            if self.current_text.strip():
                self.content_blocks.append(('list', self.current_text.strip()))
            self.current_text = ""
        elif tag == 'li' and self.in_list_item:
            self.in_list_item = False
            self.current_text += "</li>"
        elif tag in ['strong', 'b']:
            self.in_strong = False
        elif tag in ['em', 'i']:
            self.in_em = False
        elif tag == 'a':
            self.in_link = False
            self.link_href = None

    def handle_data(self, data):
        """Handle text content"""
        if self.in_nav or self.in_header or self.in_footer or not self.in_main_content:
            return

        if not (self.in_paragraph or self.in_heading or self.in_list):
            return

        # Clean and format text
        text = data.strip()
        if not text:
            return

        # Apply formatting
        if self.in_strong:
            text = f"<strong>{text}</strong>"
        if self.in_em:
            text = f"<em>{text}</em>"
        if self.in_link and self.link_href:
            text = f'<a href="{self.link_href}">{text}</a>'

        self.current_text += text + " "


class Command(BaseCommand):
    help = 'Scrape full article content from current VPQ website'

    def add_arguments(self, parser):
        parser.add_argument(
            '--slug',
            type=str,
            help='Import only specific article by slug'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Re-import all articles even if content exists'
        )
        parser.add_argument(
            '--limit',
            type=int,
            help='Only import first N articles (for testing)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be imported without making changes'
        )

    def handle(self, *args, **options):
        base_url = "https://victimespesticidesquebec.org/presse/"

        # Get articles to process
        if options['slug']:
            articles = ActualitePage.objects.filter(slug=options['slug'])
            if not articles.exists():
                self.stdout.write(self.style.ERROR(f'Article with slug "{options["slug"]}" not found'))
                return
        else:
            articles = ActualitePage.objects.live().order_by('-date_publication')
            if options['limit']:
                articles = articles[:options['limit']]

        self.stdout.write(self.style.SUCCESS(f'Processing {articles.count()} articles...'))

        success_count = 0
        error_count = 0
        skipped_count = 0

        for article in articles:
            url = f"{base_url}{article.slug}/"
            self.stdout.write(f'\nProcessing: {article.title}')
            self.stdout.write(f'URL: {url}')

            try:
                # Fetch article HTML
                with urllib.request.urlopen(url, timeout=10) as response:
                    if response.status != 200:
                        self.stdout.write(self.style.ERROR(f'  ✗ HTTP {response.status}'))
                        error_count += 1
                        continue

                    html_content = response.read().decode('utf-8')

                # Parse HTML to extract content
                parser = ArticleContentParser()
                parser.feed(html_content)

                if not parser.content_blocks:
                    self.stdout.write(self.style.WARNING(f'  ! No content extracted'))
                    error_count += 1
                    continue

                # Convert to Wagtail StreamField format
                streamfield_content = self.convert_to_streamfield(parser.content_blocks)

                if options['dry_run']:
                    self.stdout.write(self.style.WARNING(f'  [DRY RUN] Would update with {len(streamfield_content)} blocks'))
                    self.stdout.write(f'  Preview: {streamfield_content[:2]}...')
                    success_count += 1
                else:
                    # Update article content
                    article.corps = streamfield_content
                    article.save()
                    article.save_revision().publish()
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Updated with {len(streamfield_content)} content blocks'))
                    success_count += 1

            except urllib.error.HTTPError as e:
                self.stdout.write(self.style.ERROR(f'  ✗ HTTP Error: {e.code}'))
                error_count += 1
            except urllib.error.URLError as e:
                self.stdout.write(self.style.ERROR(f'  ✗ URL Error: {e.reason}'))
                error_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Error: {str(e)}'))
                error_count += 1

        # Summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'✓ Successfully processed: {success_count}'))
        if error_count:
            self.stdout.write(self.style.ERROR(f'✗ Errors: {error_count}'))
        if skipped_count:
            self.stdout.write(self.style.WARNING(f'! Skipped: {skipped_count}'))

    def convert_to_streamfield(self, content_blocks):
        """Convert parsed content blocks to Wagtail StreamField format"""
        streamfield = []

        for block_type, content in content_blocks:
            if block_type == 'paragraph':
                # Wrap in paragraph tags
                streamfield.append(('paragraphe', f'<p>{content}</p>'))
            elif block_type == 'heading':
                # Extract heading text and add as title block
                # Then add heading content as rich text
                heading_text = re.sub(r'<[^>]+>', '', content)  # Strip tags
                streamfield.append(('titre', heading_text))
            elif block_type == 'list':
                # Add list as rich text paragraphe block
                streamfield.append(('paragraphe', content))

        return streamfield
