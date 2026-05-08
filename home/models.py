from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class HomePage(Page):
    """Page d'accueil du site"""

    introduction = RichTextField(
        blank=True,
        verbose_name="Introduction",
        help_text="Texte d'introduction de la page d'accueil"
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
        ('quick_actions', blocks.StructBlock([
            ('titre', blocks.CharBlock(label="Titre de la section", default="Agissez maintenant")),
            ('actions', blocks.ListBlock(
                blocks.StructBlock([
                    ('titre', blocks.CharBlock(label="Titre de l'action")),
                    ('description', blocks.CharBlock(label="Description courte", max_length=100)),
                    ('lien', blocks.URLBlock(label="Lien")),
                    ('icone', blocks.ChoiceBlock(
                        choices=[
                            ('voice', 'Voix/Témoignage'),
                            ('alert', 'Alerte/Risque'),
                            ('help', 'Aide/Support'),
                            ('leaf', 'Nature/Alternative'),
                            ('heart', 'Soutien/Don'),
                            ('info', 'Information'),
                        ],
                        label="Icône"
                    )),
                ])
            )),
        ], label="Actions rapides", icon="tasks")),
        ('stats_block', blocks.StructBlock([
            ('titre', blocks.CharBlock(label="Titre de la section", default="L'impact en chiffres")),
            ('statistiques', blocks.ListBlock(
                blocks.StructBlock([
                    ('chiffre', blocks.CharBlock(label="Chiffre", max_length=20)),
                    ('unite', blocks.CharBlock(label="Unité", max_length=30, required=False)),
                    ('description', blocks.CharBlock(label="Description", max_length=100)),
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
        ], label="Statistiques", icon="order")),
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
        ('mission_cards', blocks.StructBlock([
            ('titre', blocks.CharBlock(label="Titre de la section", default="Notre mission")),
            ('cartes', blocks.ListBlock(
                blocks.StructBlock([
                    ('titre', blocks.CharBlock(label="Titre")),
                    ('description', blocks.TextBlock(label="Description")),
                    ('icone', blocks.ChoiceBlock(
                        choices=[
                            ('voice', 'Voix'),
                            ('awareness', 'Sensibilisation'),
                            ('alternative', 'Alternative'),
                            ('support', 'Soutien'),
                        ],
                        label="Icône"
                    )),
                ])
            )),
        ], label="Cartes de mission", icon="grip")),
        ('cta_final', blocks.StructBlock([
            ('titre', blocks.CharBlock(label="Titre")),
            ('texte', blocks.TextBlock(label="Texte")),
            ('texte_bouton', blocks.CharBlock(label="Texte du bouton")),
            ('lien_bouton', blocks.URLBlock(label="Lien du bouton")),
            ('couleur_fond', blocks.ChoiceBlock(
                choices=[
                    ('green', 'Vert'),
                    ('gray', 'Gris'),
                ],
                default='green',
                label="Couleur de fond"
            )),
        ], label="Appel à l'action final", icon="pick")),
        ('paragraphe', blocks.RichTextBlock(
            label="Paragraphe",
            features=['bold', 'italic', 'link', 'ol', 'ul', 'h2', 'h3']
        )),
        ('titre', blocks.CharBlock(
            label="Titre de section",
            form_classname="full title"
        )),
        ('image', ImageChooserBlock(label="Image")),
        ('appel_action', blocks.StructBlock([
            ('titre', blocks.CharBlock(label="Titre")),
            ('texte', blocks.TextBlock(label="Texte")),
            ('lien', blocks.URLBlock(label="Lien", required=False)),
            ('texte_bouton', blocks.CharBlock(label="Texte du bouton", required=False)),
        ], label="Appel à l'action")),
        ('dernieres_actualites', blocks.StructBlock([
            ('titre', blocks.CharBlock(label="Titre de la section", default="Dernières actualités")),
            ('nombre_actualites', blocks.IntegerBlock(
                label="Nombre d'actualités à afficher",
                default=3,
                min_value=1,
                max_value=6
            )),
            ('afficher_vedettes_seulement', blocks.BooleanBlock(
                label="Afficher seulement les actualités en vedette",
                required=False,
                default=False,
                help_text="Si activé, affiche uniquement les actualités marquées 'mise en vedette'"
            )),
            ('texte_bouton', blocks.CharBlock(
                label="Texte du bouton 'Voir toutes les actualités'",
                default="Voir toutes les actualités"
            )),
        ], label="Dernières actualités", icon="doc-full-inverse")),
    ], use_json_field=True, blank=True, verbose_name="Contenu principal")

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        FieldPanel('corps'),
    ]

    class Meta:
        verbose_name = "Page d'accueil"
        verbose_name_plural = "Pages d'accueil"

    def get_context(self, request):
        context = super().get_context(request)
        # Get featured actualites for homepage
        from actualites.models import ActualitePage
        actualites_vedette = ActualitePage.objects.live().filter(
            mise_en_vedette=True
        ).order_by('-date_publication')[:3]
        context['actualites_vedette'] = actualites_vedette
        return context
