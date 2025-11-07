from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from modelcluster.fields import ParentalKey


class StandardPage(Page):
    """Page d'information standard avec contenu flexible"""

    introduction = models.TextField(
        blank=True,
        verbose_name="Introduction",
        help_text="Introduction qui apparaîtra en haut de la page"
    )

    corps = StreamField([
        ('paragraphe', blocks.RichTextBlock(
            label="Paragraphe",
            features=['bold', 'italic', 'link', 'ol', 'ul', 'h2', 'h3', 'h4']
        )),
        ('titre', blocks.CharBlock(
            label="Titre de section",
            form_classname="full title"
        )),
        ('image', ImageChooserBlock(label="Image")),
        ('citation', blocks.BlockQuoteBlock(label="Citation")),
        ('appel_action', blocks.StructBlock([
            ('titre', blocks.CharBlock(label="Titre")),
            ('texte', blocks.TextBlock(label="Texte")),
            ('lien', blocks.URLBlock(label="Lien", required=False)),
            ('texte_bouton', blocks.CharBlock(label="Texte du bouton", required=False)),
        ], label="Appel à l'action")),
        ('html_brut', blocks.RawHTMLBlock(
            label="HTML brut",
            help_text="Utiliser avec précaution"
        )),
    ], use_json_field=True, blank=True, verbose_name="Corps de la page")

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        FieldPanel('corps'),
    ]

    class Meta:
        verbose_name = "Page standard"
        verbose_name_plural = "Pages standards"


class FormField(AbstractFormField):
    """Champ de formulaire pour ContactPage"""
    page = ParentalKey(
        'ContactPage',
        on_delete=models.CASCADE,
        related_name='form_fields'
    )


class ContactPage(AbstractEmailForm):
    """Page de contact avec formulaire"""

    introduction = RichTextField(
        blank=True,
        verbose_name="Introduction"
    )

    message_remerciement = RichTextField(
        blank=True,
        verbose_name="Message de remerciement",
        help_text="Message affiché après la soumission du formulaire"
    )

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('introduction'),
        InlinePanel('form_fields', label="Champs du formulaire"),
        FieldPanel('message_remerciement'),
        FieldPanel('to_address'),
        FieldPanel('from_address'),
        FieldPanel('subject'),
    ]

    class Meta:
        verbose_name = "Page de contact"
        verbose_name_plural = "Pages de contact"
