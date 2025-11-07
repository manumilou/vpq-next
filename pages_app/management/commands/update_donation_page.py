from django.core.management.base import BaseCommand
from pages_app.models import StandardPage


class Command(BaseCommand):
    help = 'Update the Soutenez VPQ page with content from the original site'

    def handle(self, *args, **options):
        try:
            donation_page = StandardPage.objects.get(slug='soutenez-vpq')
        except StandardPage.DoesNotExist:
            self.stdout.write(self.style.ERROR('Page "Soutenez VPQ" not found'))
            return

        # Update introduction
        donation_page.introduction = "Victimes des pesticides du Québec a besoin de votre appui !"

        # Update content blocks with original content
        donation_page.corps = [
            ('paragraphe', '<p><strong>Vos dons financent l\'accompagnement des personnes affectées et de leur famille, ainsi que le travail de prévention des risques sur la santé associés à l\'exposition aux pesticides.</strong></p><p>Grâce à votre générosité, nous pouvons conserver notre indépendance et poursuivre notre mission de défense des droits des victimes et de promotion d\'un Québec en santé.</p>'),

            ('alerte', {
                'type': 'info',
                'titre': 'Dons mensuels',
                'message': 'Dans la mesure du possible, nous privilégions les dons mensuels qui nous permettent de mieux planifier nos actions et notre budget.',
            }),

            ('zeffy_donation', {
                'titre': 'Faire un don',
                'description': 'Chaque contribution, petite ou grande, fait une différence. Merci de votre générosité !',
                'form_url': 'https://www.zeffy.com/embed/donation-form/victimes-des-pesticides-du-quebec',
                'hauteur': 900,
            }),

            ('alerte', {
                'type': 'success',
                'titre': 'Organisme de bienfaisance enregistré',
                'message': 'Victimes des pesticides du Québec est une initiative de l\'Association pour la santé publique du Québec (ASPQ), organisme de bienfaisance enregistré auprès de l\'Agence du revenu du Canada. Tous les dons de 20$ et plus donnent droit à un reçu fiscal.',
            }),

            ('paragraphe', '<p><em>Note : Victimes des pesticides du Québec est devenue une initiative de l\'Association pour la santé publique du Québec (ASPQ) en 2025, après avoir opéré comme organisme à but non lucratif indépendant depuis sa fondation en 2019.</em></p>'),

            ('titre', 'Autres façons de nous soutenir'),

            ('grille_cartes', {
                'titre': '',
                'cartes': [
                    {
                        'icone': 'users',
                        'titre': 'Devenir membre',
                        'description': 'Rejoignez notre communauté et participez activement à notre mission de défense des victimes des pesticides.',
                        'lien': 'https://manumiloucb3680adf1.wordpress.com/devenir-membre/',
                    },
                    {
                        'icone': 'heart',
                        'titre': 'Bénévolat',
                        'description': 'Offrez votre temps et vos compétences pour soutenir nos initiatives d\'accompagnement et de prévention.',
                        'lien': '/contact/',
                    },
                    {
                        'icone': 'share',
                        'titre': 'Partagez notre cause',
                        'description': 'Aidez-nous à faire connaître notre mission et sensibiliser le public aux risques des pesticides.',
                        'lien': '',
                    },
                ]
            }),

            ('appel_action', {
                'titre': 'Des questions ?',
                'texte': 'Notre équipe est disponible pour répondre à toutes vos questions concernant les dons, le bénévolat ou l\'adhésion à notre organisation.',
                'lien': '/contact/',
                'texte_bouton': 'Nous contacter',
            }),
        ]

        # Save and publish
        donation_page.save_revision().publish()

        self.stdout.write(self.style.SUCCESS(f'Successfully updated donation page: {donation_page.title}'))
        self.stdout.write(self.style.SUCCESS(f'Updated with content from original site'))
