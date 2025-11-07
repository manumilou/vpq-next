from django.core.management.base import BaseCommand
from pages_app.models import StandardPage
from home.models import HomePage


class Command(BaseCommand):
    help = 'Create or update the Soutenez VPQ donation page with Zeffy form'

    def handle(self, *args, **options):
        # Get the homepage (parent page)
        try:
            homepage = HomePage.objects.get(slug='home')
        except HomePage.DoesNotExist:
            self.stdout.write(self.style.ERROR('HomePage not found'))
            return

        # Check if Soutenez VPQ page already exists
        try:
            donation_page = StandardPage.objects.get(slug='soutenez-vpq')
            self.stdout.write(self.style.WARNING(f'Page "Soutenez VPQ" already exists, updating...'))
        except StandardPage.DoesNotExist:
            # Create new page
            donation_page = StandardPage(
                title='Soutenez VPQ',
                slug='soutenez-vpq',
            )
            homepage.add_child(instance=donation_page)
            self.stdout.write(self.style.SUCCESS('Created new "Soutenez VPQ" page'))

        # Set introduction
        donation_page.introduction = "Votre soutien est essentiel pour notre mission de défendre les droits des victimes des pesticides et promouvoir un Québec en santé."

        # Create content blocks
        donation_page.corps = [
            ('paragraphe', '<p>Victimes des pesticides du Québec (VPQ) est une organisation à but non lucratif qui œuvre pour la reconnaissance et la défense des droits des personnes affectées par l\'exposition aux pesticides.</p><p>Vos dons nous permettent de :</p><ul><li>Accompagner les victimes dans leurs démarches d\'indemnisation</li><li>Sensibiliser le public aux risques des pesticides</li><li>Promouvoir des alternatives non toxiques</li><li>Soutenir la recherche scientifique sur les impacts sanitaires</li></ul>'),

            ('zeffy_donation', {
                'titre': 'Faire un don',
                'description': 'Chaque contribution, petite ou grande, fait une différence. Merci de votre générosité !',
                'form_url': 'https://www.zeffy.com/embed/donation-form/victimes-des-pesticides-du-quebec',
                'hauteur': 900,
            }),

            ('alerte', {
                'type': 'info',
                'titre': 'Reçu fiscal',
                'message': 'VPQ est un organisme à but non lucratif. Tous les dons de 20$ et plus sont admissibles à un reçu fiscal pour fin d\'impôt.',
            }),

            ('titre', 'Autres façons de nous soutenir'),

            ('grille_cartes', {
                'titre': '',
                'cartes': [
                    {
                        'icone': 'users',
                        'titre': 'Devenir membre',
                        'description': 'Rejoignez notre communauté et participez activement à notre mission.',
                        'lien': '/a-propos/',
                    },
                    {
                        'icone': 'heart',
                        'titre': 'Bénévolat',
                        'description': 'Offrez votre temps et vos compétences pour soutenir nos initiatives.',
                        'lien': '/contact/',
                    },
                    {
                        'icone': 'users',
                        'titre': 'Partagez notre cause',
                        'description': 'Aidez-nous à faire connaître notre mission sur les réseaux sociaux.',
                        'lien': '',
                    },
                ]
            }),

            ('appel_action', {
                'titre': 'Des questions sur les dons ?',
                'texte': 'Notre équipe est disponible pour répondre à toutes vos questions concernant les dons et le soutien à notre organisation.',
                'lien': '/contact/',
                'texte_bouton': 'Nous contacter',
            }),
        ]

        # Save and publish
        donation_page.save_revision().publish()

        self.stdout.write(self.style.SUCCESS(f'Successfully created/updated donation page: {donation_page.title}'))
        self.stdout.write(self.style.SUCCESS(f'Page URL: /soutenez-vpq/'))
        self.stdout.write(self.style.SUCCESS(f'Added Zeffy donation form with {len(donation_page.corps)} blocks'))
