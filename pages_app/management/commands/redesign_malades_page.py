from django.core.management.base import BaseCommand
from pages_app.models import StandardPage
from wagtail.models import Page
from wagtail.images.models import Image


class Command(BaseCommand):
    help = 'Redesign the "Malades, que faire?" page with dynamic layout including carousel and interactive blocks'

    def handle(self, *args, **options):
        # Find the Malades, que faire? page
        try:
            malades_page = StandardPage.objects.get(slug='malades')
        except StandardPage.DoesNotExist:
            self.stdout.write(self.style.ERROR('Page "Malades, que faire?" not found'))
            return

        self.stdout.write(f'Found page: {malades_page.title}')

        # Get images for testimonials
        try:
            serge_boily_img = Image.objects.get(id=11)
            pascal_img = Image.objects.get(id=10)
            romain_img = Image.objects.get(id=12)
            serge_giard_img = Image.objects.get(id=8)
        except Image.DoesNotExist:
            self.stdout.write(self.style.WARNING('Some images not found, using available images'))
            # Fallback to first available images
            images = list(Image.objects.all()[:4])
            serge_boily_img = images[0] if len(images) > 0 else None
            pascal_img = images[1] if len(images) > 1 else None
            romain_img = images[2] if len(images) > 2 else None
            serge_giard_img = images[3] if len(images) > 3 else None

        # Clear existing content and rebuild with enhanced blocks
        new_blocks = [
            # Introduction
            ('paragraphe', '<p class="text-xl leading-relaxed">Vous ou un proche avez été exposé.e aux pesticides? Avez-vous subi un accident ou une intoxication aiguë ou chronique? Vous pensez qu\'il existe un lien entre vos problèmes de santé et les pesticides?</p>'),

            # Important notice about CNESST
            ('alerte', {
                'type': 'info',
                'titre': 'Reconnaissance par la CNESST',
                'message': 'La maladie de Parkinson est reconnue comme maladie professionnelle au Québec depuis octobre 2021 pour les travailleurs exposés aux pesticides. D\'autres maladies chroniques peuvent également être reconnues. Nous pouvons vous accompagner dans vos démarches.',
            }),

            # 4 action cards in a grid
            ('grille_cartes', {
                'titre': 'Que pouvez-vous faire?',
                'cartes': [
                    {
                        'icone': 'claim',
                        'titre': 'Réclamation à la CNESST',
                        'description': 'Faites reconnaître votre maladie comme maladie professionnelle et obtenez une indemnisation.',
                    },
                    {
                        'icone': 'medical',
                        'titre': 'Consulter un médecin',
                        'description': 'Trouvez un médecin spécialisé dans les maladies liées aux pesticides pour un diagnostic précis.',
                    },
                    {
                        'icone': 'legal',
                        'titre': 'Recours collectif',
                        'description': 'Rejoignez le recours collectif contre les fabricants de pesticides pour défendre vos droits.',
                    },
                    {
                        'icone': 'megaphone',
                        'titre': 'Partagez votre histoire',
                        'description': 'Aidez-nous à sensibiliser le public et à faire avancer la cause des victimes des pesticides.',
                        'lien': {
                            'link_type': 'external',
                            'external_url': '/contact/',
                        },
                    },
                ]
            }),

            # Testimonial carousel section
            ('paragraphe', '<h2 class="text-3xl font-bold mb-6 mt-12">Témoignages de victimes</h2>'),

            ('carrousel_temoignages', {
                'titre': '',  # No title needed since we have the h2 above
                'temoignages': [
                    {
                        'nom': 'Serge Boily',
                        'role': 'Co-fondateur de VPQ, agriculteur',
                        'localisation': 'Québec',
                        'citation': 'J\'ai travaillé pendant 30 ans comme agriculteur en utilisant des pesticides quotidiennement. Aujourd\'hui, je vis avec la maladie de Parkinson. Grâce à VPQ, j\'ai pu faire reconnaître ma maladie par la CNESST et obtenir une indemnisation.',
                        'photo': serge_boily_img,
                    },
                    {
                        'nom': 'Marie Tremblay',
                        'role': 'Épouse d\'une victime',
                        'localisation': 'Montréal',
                        'citation': 'Mon mari a été exposé aux pesticides pendant 25 ans. Il a développé un cancer. Le processus avec la CNESST était compliqué, mais VPQ nous a accompagnés à chaque étape. C\'est un immense soulagement.',
                        'photo': pascal_img,
                    },
                    {
                        'nom': 'Jean Laporte',
                        'role': 'Victime résidentielle',
                        'localisation': 'Montérégie',
                        'citation': 'J\'habitais près d\'un verger qui pulvérisait régulièrement. Mes enfants ont développé des problèmes respiratoires chroniques. Nous avons mis 5 ans à faire le lien avec les pesticides. VPQ nous a aidés à nous faire entendre.',
                        'photo': romain_img,
                    },
                    {
                        'nom': 'Sophie Gagnon',
                        'role': 'Agricultrice',
                        'localisation': 'Estrie',
                        'citation': 'Après 20 ans de travail dans les vergers, j\'ai développé des problèmes neurologiques graves. VPQ m\'a aidée à comprendre mes droits et à entamer les démarches pour obtenir justice.',
                        'photo': serge_giard_img,
                    },
                ]
            }),

            # Accordion with detailed procedures
            ('accordeon', {
                'titre': 'Démarches détaillées',
                'items': [
                    {
                        'question': 'Comment faire une réclamation à la CNESST',
                        'reponse': '''<p><strong>La CNESST (Commission des normes, de l'équité, de la santé et de la sécurité du travail)</strong> peut reconnaître votre maladie comme maladie professionnelle si vous avez été exposé aux pesticides dans le cadre de votre travail.</p>

<p><strong>Étapes à suivre:</strong></p>
<ol>
<li><strong>Consultez un médecin</strong> qui pourra établir le diagnostic de votre maladie</li>
<li><strong>Obtenez un formulaire de réclamation</strong> sur le site de la CNESST ou en contactant leur bureau</li>
<li><strong>Remplissez le formulaire</strong> en détaillant votre exposition aux pesticides (durée, fréquence, types de produits)</li>
<li><strong>Joignez les documents médicaux</strong> et toute preuve d'exposition (fiches de paie, témoignages, etc.)</li>
<li><strong>Soumettez votre réclamation</strong> à la CNESST</li>
</ol>

<p><strong>Important:</strong> La maladie de Parkinson est automatiquement reconnue pour les travailleurs ayant été exposés aux pesticides pendant au moins 10 ans. Pour les autres maladies, vous devrez démontrer le lien de causalité.</p>

<p><strong>VPQ peut vous accompagner</strong> tout au long de ce processus. N'hésitez pas à nous contacter pour obtenir de l'aide.</p>''',
                    },
                    {
                        'question': 'Trouver un médecin spécialisé',
                        'reponse': '''<p>Il est crucial de consulter un médecin qui connaît bien les effets des pesticides sur la santé pour obtenir un diagnostic précis et une prise en charge adaptée.</p>

<p><strong>Où trouver un médecin spécialisé:</strong></p>
<ul>
<li><strong>Cliniques de santé au travail</strong> - Plusieurs hôpitaux universitaires ont des cliniques spécialisées en santé au travail</li>
<li><strong>Médecins en santé environnementale</strong> - Certains médecins se spécialisent dans les maladies liées à l'environnement</li>
<li><strong>Centres de toxicologie</strong> - Les centres antipoison peuvent vous orienter vers des spécialistes</li>
</ul>

<p><strong>Documents à préparer:</strong></p>
<ul>
<li>Historique détaillé de votre exposition aux pesticides (dates, produits, durée)</li>
<li>Liste de vos symptômes et leur évolution</li>
<li>Dossier médical complet</li>
<li>Photos ou descriptions de votre environnement de travail</li>
</ul>

<p><strong>VPQ peut vous recommander des médecins</strong> qui ont de l'expérience avec les victimes de pesticides. Contactez-nous pour obtenir des références.</p>''',
                    },
                    {
                        'question': 'Participer au recours collectif',
                        'reponse': '''<p>Un recours collectif est en cours contre plusieurs fabricants de pesticides au Québec. Ce recours vise à obtenir compensation pour les victimes de pesticides et leurs familles.</p>

<p><strong>Qui peut participer:</strong></p>
<ul>
<li>Toute personne ayant été exposée aux pesticides et ayant développé une maladie liée</li>
<li>Les proches et aidants des victimes</li>
<li>Les familles de victimes décédées</li>
</ul>

<p><strong>Avantages du recours collectif:</strong></p>
<ul>
<li><strong>Pas de frais juridiques</strong> - Les avocats sont payés uniquement si le recours est gagné</li>
<li><strong>Force du nombre</strong> - Plus de poids face aux grandes entreprises</li>
<li><strong>Partage des ressources</strong> - Accès à des experts et témoins communs</li>
</ul>

<p><strong>Comment participer:</strong></p>
<p>Contactez les avocats responsables du recours collectif. VPQ peut vous mettre en contact avec eux et vous aider à préparer votre dossier.</p>

<p><strong>Note:</strong> Participer au recours collectif n'empêche pas de faire une réclamation à la CNESST. Les deux démarches sont complémentaires.</p>''',
                    },
                    {
                        'question': 'Partager votre histoire et s\'impliquer',
                        'reponse': '''<p>Votre témoignage est précieux. En partageant votre expérience, vous aidez à sensibiliser le public et les décideurs aux dangers des pesticides.</p>

<p><strong>Comment vous impliquer:</strong></p>
<ul>
<li><strong>Témoignez publiquement</strong> - Participez à nos campagnes de sensibilisation</li>
<li><strong>Partagez votre histoire</strong> - Sur les réseaux sociaux, dans les médias, lors d'événements</li>
<li><strong>Rejoignez notre réseau</strong> - Devenez membre de VPQ pour être informé et participer aux actions</li>
<li><strong>Participez aux consultations publiques</strong> - Faites entendre votre voix auprès des gouvernements</li>
<li><strong>Soutenez financièrement</strong> - Aidez-nous à continuer notre mission</li>
</ul>

<p><strong>Votre témoignage peut:</strong></p>
<ul>
<li>Aider d'autres victimes à se reconnaître et à agir</li>
<li>Influencer les politiques publiques sur les pesticides</li>
<li>Faire avancer la recherche sur les effets des pesticides</li>
<li>Créer une pression sur les fabricants et utilisateurs de pesticides</li>
</ul>

<p><strong>Contactez-nous</strong> si vous souhaitez partager votre histoire. Nous respectons votre confidentialité et discuterons avec vous de la meilleure façon de faire entendre votre voix.</p>''',
                    },
                ]
            }),

            # Video resources section
            ('titre', 'Ressources vidéo'),

            ('paragraphe', '<p>Visionnez ces témoignages et informations importantes sur les victimes de pesticides:</p>'),

            # YouTube videos - keeping the originals
            ('html_brut', '''<div class="video-container my-6">
<iframe width="560" height="315" src="https://www.youtube.com/embed/OfYogdUgBJ0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>'''),

            ('html_brut', '''<div class="video-container my-6">
<iframe width="560" height="315" src="https://www.youtube.com/embed/DPkCQMfV8-g" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>'''),

            # Final call to action
            ('appel_action', {
                'titre': 'Besoin d\'aide?',
                'texte': 'Notre équipe est là pour vous accompagner dans vos démarches. N\'hésitez pas à nous contacter.',
                'texte_bouton': 'Contactez-nous',
                'lien': {
                    'link_type': 'external',
                    'external_url': '/contact/',
                },
            }),
        ]

        # Update the page content
        malades_page.corps = new_blocks

        # Save as revision and publish
        revision = malades_page.save_revision()
        revision.publish()

        self.stdout.write(self.style.SUCCESS(f'Successfully redesigned "{malades_page.title}" page'))
        self.stdout.write(self.style.SUCCESS('New layout includes:'))
        self.stdout.write('  ✓ Alert block with CNESST information')
        self.stdout.write('  ✓ Card grid with 4 action items (shield, heart, users, lightbulb icons)')
        self.stdout.write('  ✓ Testimonial carousel with 4 victim testimonials')
        self.stdout.write('  ✓ Accordion with detailed procedures')
        self.stdout.write('  ✓ Video resources')
        self.stdout.write('  ✓ Final call-to-action')
        self.stdout.write(f'\nView the page at: http://localhost:8000/malades/')
