from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock
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
        ('image_avec_legende', blocks.StructBlock([
            ('image', ImageChooserBlock(label="Image")),
            ('legende', blocks.CharBlock(label="Légende", required=False)),
            ('credit', blocks.CharBlock(label="Crédit photo", required=False)),
        ], label="Image avec légende", icon="image")),
        ('citation', blocks.BlockQuoteBlock(label="Citation")),
        ('tableau', TableBlock(
            label="Tableau",
            help_text="Tableau avec lignes et colonnes"
        )),
        ('temoignage', blocks.StructBlock([
            ('citation', blocks.TextBlock(label="Citation")),
            ('auteur', blocks.CharBlock(label="Auteur")),
            ('role', blocks.CharBlock(label="Rôle/Titre", required=False)),
            ('photo', ImageChooserBlock(label="Photo", required=False)),
        ], label="Témoignage", icon="user")),
        ('deux_colonnes', blocks.StructBlock([
            ('colonne_gauche', blocks.RichTextBlock(
                label="Colonne gauche",
                features=['bold', 'italic', 'link', 'ol', 'ul']
            )),
            ('colonne_droite', blocks.RichTextBlock(
                label="Colonne droite",
                features=['bold', 'italic', 'link', 'ol', 'ul']
            )),
        ], label="Deux colonnes", icon="horizontalrule")),
        ('carte_personne', blocks.StructBlock([
            ('nom', blocks.CharBlock(label="Nom")),
            ('role', blocks.CharBlock(label="Rôle")),
            ('photo', ImageChooserBlock(label="Photo", required=False)),
            ('biographie', blocks.TextBlock(label="Biographie")),
            ('email', blocks.EmailBlock(label="Email", required=False)),
        ], label="Carte de personne (équipe)", icon="user")),
        ('grille_cartes', blocks.StructBlock([
            ('titre', blocks.CharBlock(label="Titre de la section", required=False)),
            ('cartes', blocks.ListBlock(
                blocks.StructBlock([
                    ('icone', blocks.ChoiceBlock(
                        label="Icône",
                        choices=[
                            ('info', 'Information'),
                            ('heart', 'Coeur'),
                            ('users', 'Utilisateurs'),
                            ('check', 'Vérification'),
                            ('star', 'Étoile'),
                            ('book', 'Livre'),
                            ('lightbulb', 'Ampoule'),
                            ('shield', 'Bouclier'),
                        ],
                        default='info'
                    )),
                    ('titre', blocks.CharBlock(label="Titre")),
                    ('description', blocks.TextBlock(label="Description")),
                    ('lien', blocks.URLBlock(label="Lien", required=False)),
                ])
            )),
        ], label="Grille de cartes", icon="grip")),
        ('statistiques', blocks.StructBlock([
            ('titre', blocks.CharBlock(label="Titre de la section", required=False)),
            ('stats', blocks.ListBlock(
                blocks.StructBlock([
                    ('chiffre', blocks.CharBlock(label="Chiffre")),
                    ('unite', blocks.CharBlock(label="Unité", required=False)),
                    ('description', blocks.CharBlock(label="Description")),
                ])
            )),
        ], label="Statistiques", icon="list-ol")),
        ('alerte', blocks.StructBlock([
            ('type', blocks.ChoiceBlock(
                label="Type",
                choices=[
                    ('info', 'Information (bleu)'),
                    ('success', 'Succès (vert)'),
                    ('warning', 'Attention (orange)'),
                    ('danger', 'Danger (rouge)'),
                ],
                default='info'
            )),
            ('titre', blocks.CharBlock(label="Titre", required=False)),
            ('message', blocks.TextBlock(label="Message")),
        ], label="Alerte/Notice", icon="warning")),
        ('accordeon', blocks.StructBlock([
            ('titre', blocks.CharBlock(label="Titre de la section", required=False)),
            ('items', blocks.ListBlock(
                blocks.StructBlock([
                    ('question', blocks.CharBlock(label="Question/Titre")),
                    ('reponse', blocks.RichTextBlock(
                        label="Réponse/Contenu",
                        features=['bold', 'italic', 'link', 'ol', 'ul']
                    )),
                ])
            )),
        ], label="Accordéon (FAQ)", icon="list-ul")),
        ('appel_action', blocks.StructBlock([
            ('titre', blocks.CharBlock(label="Titre")),
            ('texte', blocks.TextBlock(label="Texte")),
            ('lien', blocks.URLBlock(label="Lien", required=False)),
            ('texte_bouton', blocks.CharBlock(label="Texte du bouton", required=False)),
        ], label="Appel à l'action")),
        ('zeffy_donation', blocks.StructBlock([
            ('titre', blocks.CharBlock(label="Titre", default="Soutenez notre cause")),
            ('description', blocks.TextBlock(label="Description", required=False)),
            ('form_url', blocks.URLBlock(
                label="URL du formulaire Zeffy",
                default="https://www.zeffy.com/embed/donation-form/victimes-des-pesticides-du-quebec",
                help_text="URL d'intégration Zeffy (ex: https://www.zeffy.com/embed/donation-form/...)"
            )),
            ('hauteur', blocks.IntegerBlock(
                label="Hauteur du formulaire (px)",
                default=800,
                help_text="Hauteur en pixels (recommandé: 800-1000)"
            )),
        ], label="Formulaire de don Zeffy", icon="form")),
        ('mailchimp_signup', blocks.StructBlock([
            ('titre', blocks.CharBlock(label="Titre", default="Restez informé·e")),
            ('description', blocks.TextBlock(
                label="Description",
                default="Inscrivez-vous à notre infolettre pour recevoir nos actualités et rester informé de nos actions."
            )),
            ('action_url', blocks.URLBlock(
                label="URL d'action Mailchimp",
                default="https://victimespesticidesquebec.us2.list-manage.com/subscribe/post?u=67c56a4224e79e980c9022db9&id=6e5f62b588",
                help_text="URL du formulaire Mailchimp"
            )),
            ('bouton_text', blocks.CharBlock(label="Texte du bouton", default="S'abonner")),
            ('style', blocks.ChoiceBlock(
                label="Style",
                choices=[
                    ('simple', 'Simple (inline)'),
                    ('box', 'Boîte mise en valeur'),
                ],
                default='box'
            )),
        ], label="Inscription infolettre Mailchimp", icon="mail")),
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
