from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet


@register_snippet
class Categorie(models.Model):
    """Catégorie d'actualité"""
    nom = models.CharField(max_length=255, verbose_name="Nom")
    slug = models.SlugField(unique=True, verbose_name="Identifiant URL")
    description = models.TextField(blank=True, verbose_name="Description")

    panels = [
        FieldPanel('nom'),
        FieldPanel('slug'),
        FieldPanel('description'),
    ]

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.nom


@register_snippet
class Auteur(models.Model):
    """Auteur d'actualité"""
    nom = models.CharField(max_length=255, verbose_name="Nom")
    prenom = models.CharField(max_length=255, verbose_name="Prénom")
    biographie = RichTextField(blank=True, verbose_name="Biographie")
    courriel = models.EmailField(blank=True, verbose_name="Courriel")
    photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Photo"
    )

    panels = [
        FieldPanel('prenom'),
        FieldPanel('nom'),
        FieldPanel('biographie'),
        FieldPanel('courriel'),
        FieldPanel('photo'),
    ]

    class Meta:
        verbose_name = "Auteur"
        verbose_name_plural = "Auteurs"

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"


class ActualitePage(Page):
    """Page d'actualité avec contenu flexible"""

    date_publication = models.DateField(
        verbose_name="Date de publication",
        help_text="Date à laquelle l'actualité sera publiée"
    )

    auteur = models.ForeignKey(
        Auteur,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='actualites',
        verbose_name="Auteur"
    )

    categories = models.ManyToManyField(
        Categorie,
        blank=True,
        verbose_name="Catégories"
    )

    image_principale = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Image principale"
    )

    introduction = models.TextField(
        blank=True,
        verbose_name="Introduction",
        help_text="Court résumé qui apparaîtra dans les listes"
    )

    corps = StreamField([
        ('paragraphe', blocks.RichTextBlock(
            label="Paragraphe",
            features=['bold', 'italic', 'link', 'ol', 'ul']
        )),
        ('titre', blocks.CharBlock(
            label="Titre de section",
            form_classname="full title"
        )),
        ('image', ImageChooserBlock(label="Image")),
        ('citation', blocks.BlockQuoteBlock(label="Citation")),
        ('code', blocks.TextBlock(
            label="Code",
            help_text="Bloc de code"
        )),
        ('html_brut', blocks.RawHTMLBlock(
            label="HTML brut",
            help_text="Utiliser avec précaution"
        )),
    ], use_json_field=True, blank=True, verbose_name="Corps de l'article")

    mise_en_vedette = models.BooleanField(
        default=False,
        verbose_name="Mise en vedette",
        help_text="Afficher dans la section vedette de la page d'accueil"
    )

    content_panels = Page.content_panels + [
        FieldPanel('date_publication'),
        FieldPanel('auteur'),
        FieldPanel('categories'),
        FieldPanel('image_principale'),
        FieldPanel('introduction'),
        FieldPanel('corps'),
        FieldPanel('mise_en_vedette'),
    ]

    class Meta:
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"

    def get_context(self, request):
        context = super().get_context(request)
        # Add extra context for templates
        context['categories'] = self.categories.all()
        return context


class ActualiteIndexPage(Page):
    """Page d'index pour lister toutes les actualités"""

    introduction = RichTextField(
        blank=True,
        verbose_name="Introduction"
    )

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
    ]

    class Meta:
        verbose_name = "Page d'index des actualités"
        verbose_name_plural = "Pages d'index des actualités"

    def get_context(self, request):
        context = super().get_context(request)
        # Get all published actualites, ordered by publication date
        actualites = ActualitePage.objects.live().order_by('-date_publication')
        context['actualites'] = actualites
        return context

    # Only allow ActualitePage as children
    subpage_types = ['actualites.ActualitePage']
