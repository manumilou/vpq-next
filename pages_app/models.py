from django.db import models
from django.utils.text import slugify
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock
from modelcluster.fields import ParentalKey


class LinkBlock(blocks.StructBlock):
    """Block for internal, external, or same-page anchor links"""
    link_type = blocks.ChoiceBlock(
        label="Type de lien",
        choices=[
            ('internal', 'Page interne'),
            ('external', 'Lien externe'),
            ('anchor', 'Ancre sur cette page'),
        ],
        default='internal'
    )
    internal_page = blocks.PageChooserBlock(
        label="Page interne",
        required=False,
        help_text="Choisir une page du site"
    )
    external_url = blocks.URLBlock(
        label="URL externe",
        required=False,
        help_text="Ex: https://example.com"
    )
    anchor_id = blocks.CharBlock(
        label="Ancre",
        required=False,
        help_text="Ex: reclamation-a-la-cnesst — sans le #"
    )

    class Meta:
        icon = 'link'
        label = 'Lien'

    def get_url(self, value):
        """Get the appropriate URL based on link type"""
        if value.get('link_type') == 'internal' and value.get('internal_page'):
            return value['internal_page'].url
        elif value.get('link_type') == 'external' and value.get('external_url'):
            return value['external_url']
        elif value.get('link_type') == 'anchor' and value.get('anchor_id'):
            return f"#{slugify(value['anchor_id'].lstrip('#'))}"
        return '#'


class StandardPage(Page):
    """Page d'information standard avec contenu flexible"""

    introduction = models.TextField(
        blank=True,
        verbose_name="Introduction",
        help_text="Introduction qui apparaîtra en haut de la page"
    )

    corps = StreamField([
        ('hero_block', blocks.StructBlock([
            ('image_fond', ImageChooserBlock(label="Image de fond")),
            ('titre_principal', blocks.CharBlock(label="Titre principal")),
            ('sous_titre', blocks.CharBlock(label="Sous-titre", required=False)),
            ('texte_bouton', blocks.CharBlock(label="Texte du bouton", required=False)),
            ('lien_bouton', blocks.URLBlock(label="Lien du bouton", required=False)),
            ('opacite_overlay', blocks.IntegerBlock(
                label="Opacité de l'overlay (%)",
                default=40,
                min_value=0,
                max_value=80,
                help_text="Assombrit l'image pour améliorer la lisibilité du texte (0-80%)"
            )),
        ], label="Bloc héro pleine largeur", icon="image")),
        ('problematique_block', blocks.StructBlock([
            ('titre', blocks.CharBlock(label="Titre")),
            ('contenu', blocks.RichTextBlock(
                label="Contenu",
                features=['bold', 'italic', 'link', 'ol', 'ul']
            )),
            ('image', ImageChooserBlock(label="Image", required=False)),
            ('position_image', blocks.ChoiceBlock(
                choices=[
                    ('left', 'Gauche'),
                    ('right', 'Droite'),
                ],
                default='right',
                label="Position de l'image"
            )),
        ], label="Bloc problématique", icon="doc-full")),
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
        ], label="Carte de personne (unique)", icon="user")),
        ('grille_equipe', blocks.StructBlock([
            ('titre', blocks.CharBlock(label="Titre de la section", required=False)),
            ('description', blocks.RichTextBlock(
                label="Description",
                required=False,
                features=['bold', 'italic', 'link']
            )),
            ('personnes', blocks.ListBlock(
                blocks.StructBlock([
                    ('photo', ImageChooserBlock(label="Photo", required=False)),
                    ('nom', blocks.CharBlock(label="Nom")),
                    ('role', blocks.CharBlock(label="Rôle")),
                    ('biographie', blocks.TextBlock(label="Biographie courte", required=False)),
                    ('email', blocks.EmailBlock(label="Email", required=False)),
                    ('telephone', blocks.CharBlock(label="Téléphone", required=False)),
                ])
            )),
        ], label="Grille d'équipe", icon="group")),
        ('grille_cartes', blocks.StructBlock([
            ('titre', blocks.CharBlock(label="Titre de la section", required=False)),
            ('cartes', blocks.ListBlock(
                blocks.StructBlock([
                    ('icone', blocks.ChoiceBlock(
                        label="Icône",
                        choices=[
                            ('info', 'Information'),
                            ('medical', 'Médecin / santé'),
                            ('claim', 'Réclamation / dossier'),
                            ('legal', 'Recours juridique'),
                            ('megaphone', 'Témoignage / sensibilisation'),
                            ('heart', 'Coeur / entraide'),
                            ('users', 'Groupe / communauté'),
                            ('check', 'Vérification'),
                            ('star', 'Étoile'),
                            ('book', 'Livre / recherche'),
                            ('lightbulb', 'Idée / solution'),
                            ('shield', 'Protection'),
                            ('share', 'Partage'),
                            ('leaf', 'Environnement'),
                            ('broadcast', 'Mobilisation'),
                        ],
                        default='info'
                    )),
                    ('titre', blocks.CharBlock(label="Titre")),
                    ('description', blocks.TextBlock(label="Description")),
                    ('lien', LinkBlock(label="Lien", required=False)),
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
                    ('source_num', blocks.IntegerBlock(label="N° de source (exposant)", required=False, help_text="Numéro renvoyant à la liste des sources")),
                ])
            )),
            ('sources', blocks.ListBlock(
                blocks.StructBlock([
                    ('texte', blocks.CharBlock(label="Référence")),
                    ('url', blocks.URLBlock(label="Lien", required=False)),
                ]),
                label="Sources",
                required=False,
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
            ('message', blocks.RichTextBlock(
                label="Message",
                features=['bold', 'italic', 'link', 'ol', 'ul']
            )),
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
        ('carrousel_temoignages', blocks.StructBlock([
            ('titre', blocks.CharBlock(label="Titre de la section", required=False)),
            ('temoignages', blocks.ListBlock(
                blocks.StructBlock([
                    ('photo', ImageChooserBlock(label="Photo")),
                    ('citation', blocks.RichTextBlock(
                        label="Témoignage",
                        features=['bold', 'italic', 'link']
                    )),
                    ('nom', blocks.CharBlock(label="Nom")),
                    ('role', blocks.CharBlock(label="Rôle/Titre", required=False)),
                    ('localisation', blocks.CharBlock(label="Localisation", required=False)),
                ])
            )),
            ('defilement_auto', blocks.BooleanBlock(
                label="Défilement automatique",
                default=True,
                required=False,
                help_text="Les témoignages défileront automatiquement toutes les 5 secondes"
            )),
        ], label="Carrousel de témoignages", icon="group")),
        ('appel_action', blocks.StructBlock([
            ('titre', blocks.CharBlock(label="Titre")),
            ('texte', blocks.TextBlock(label="Texte")),
            ('lien', LinkBlock(label="Lien", required=False)),
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
        ('grille_logos', blocks.StructBlock([
            ('titre', blocks.CharBlock(label="Titre de la section", required=False)),
            ('logos', blocks.ListBlock(
                blocks.StructBlock([
                    ('nom', blocks.CharBlock(label="Nom de l'organisation")),
                    ('logo', ImageChooserBlock(label="Logo")),
                    ('lien', blocks.URLBlock(label="Lien vers le site", required=False)),
                ])
            )),
        ], label="Grille de logos", icon="image")),
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

    def get_landing_page_template(self, request, *args, **kwargs):
        """Return the landing page template after form submission"""
        return 'pages_app/contact_page_landing.html'

    class Meta:
        verbose_name = "Page de contact"
        verbose_name_plural = "Pages de contact"
