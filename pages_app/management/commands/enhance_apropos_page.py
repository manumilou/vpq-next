from django.core.management.base import BaseCommand
from pages_app.models import StandardPage
from wagtail.models import Page


class Command(BaseCommand):
    help = 'Enhance the À propos page with new visual blocks'

    def handle(self, *args, **options):
        # Find the À propos page
        try:
            apropos = StandardPage.objects.get(slug='a-propos')
        except StandardPage.DoesNotExist:
            self.stdout.write(self.style.ERROR('Page "À propos" not found'))
            return

        # Clear existing content and rebuild with enhanced blocks
        new_blocks = [
            ('titre', 'Victimes des pesticides du Québec, c\'est quoi ?'),

            ('grille_cartes', {
                'titre': 'Notre mission',
                'cartes': [
                    {
                        'icone': 'info',
                        'titre': 'Informer',
                        'description': 'Informer les personnes victimes des pesticides, leur entourage et le grand public.',
                        'lien': '',
                    },
                    {
                        'icone': 'users',
                        'titre': 'Orienter',
                        'description': 'Orienter ces personnes dans leurs démarches de soins et d\'indemnisation.',
                        'lien': '',
                    },
                    {
                        'icone': 'shield',
                        'titre': 'Mobiliser',
                        'description': 'Mobiliser toutes les parties prenantes pour prévenir les risques sur la santé associés à l\'exposition aux pesticides.',
                        'lien': '',
                    },
                    {
                        'icone': 'book',
                        'titre': 'Recherche',
                        'description': 'Diffuser et rendre accessible la recherche scientifique sur les risques liés aux pesticides.',
                        'lien': '',
                    },
                    {
                        'icone': 'lightbulb',
                        'titre': 'Promouvoir',
                        'description': 'Promouvoir des solutions non toxiques pour remplacer les pesticides.',
                        'lien': '',
                    },
                ]
            }),

            ('paragraphe', '<p><i>Victimes des pesticides du Québec</i> (VPQ) regroupe les personnes victimes des pesticides afin de défendre leurs droits et faire connaître leurs revendications et recommandations pour un Québec en santé.</p>'),

            ('deux_colonnes', {
                'colonne_gauche': '<p>Fondé en décembre 2019, VPQ consolide la mobilisation citoyenne pour la cause des victimes des pesticides. VPQ regroupe des personnes ayant été exposées aux pesticides et atteintes de maladies chroniques sévères dont le parkinson ainsi que des associations de patient.e.s inquiètes de la recrudescence des maladies associées à l\'exposition aux pesticides.</p>',
                'colonne_droite': '<p>Dès janvier 2020, VPQ entre en action et présente, dans le cadre de la modernisation du régime de santé et sécurité au travail, <a href="https://www.victimespesticidesquebec.org/20210111_Rapport_Pesticides_Maladies_chroniques_Projet_de_Loi_59.pdf">un mémoire conjoint</a> aux côtés de Parkinson Québec et obtient ainsi la reconnaissance de la maladie de Parkinson comme maladie professionnelle en octobre 2021.</p>',
            }),

            ('alerte', {
                'type': 'success',
                'titre': 'Une avancée historique',
                'message': 'Cette causalité établie par voie législative est une avancée sociale exceptionnelle pour les Québécoises et Québécois puisque la maladie de Parkinson est reconnue comme maladie professionnelle seulement en France et en Suède.',
            }),

            ('paragraphe', '<p>Depuis cette victoire, VPQ accompagne les victimes des pesticides et leurs proches dans leurs démarches auxquelles elles sont confrontées et particulièrement auprès de la CNESST, et ce, tout en travaillant avec de nombreux partenaires.</p>'),

            ('titre', 'Victimes des pesticides du Québec, c\'est qui ?'),

            ('paragraphe', '<p>Tout individu ou organisme intéressé à soutenir la mission peut <a href="https://manumiloucb3680adf1.wordpress.com/devenir-membre/">devenir membre</a>.</p>'),

            ('grille_cartes', {
                'titre': 'Les organisations membres',
                'cartes': [
                    {'icone': 'users', 'titre': 'Autisme Montréal', 'description': 'Organisation membre', 'lien': ''},
                    {'icone': 'users', 'titre': 'Parkinson Québec', 'description': 'Organisation membre', 'lien': ''},
                    {'icone': 'users', 'titre': 'Myélome Canada', 'description': 'Organisation membre', 'lien': ''},
                    {'icone': 'users', 'titre': 'Action Cancer du Sein du Québec', 'description': 'Organisation membre', 'lien': ''},
                    {'icone': 'users', 'titre': 'Vigilance OGM', 'description': 'Organisation membre', 'lien': ''},
                    {'icone': 'users', 'titre': 'Phyto-Victimes', 'description': 'Organisation membre', 'lien': ''},
                    {'icone': 'users', 'titre': 'CATTARA', 'description': 'Organisation membre', 'lien': ''},
                ]
            }),

            ('titre', 'Le conseil d\'administration'),

            ('carte_personne', {
                'nom': 'Serge Giard',
                'role': 'Cofondateur et président',
                'photo': None,
                'biographie': 'Agriculteur à la retraite atteint de la maladie de Parkinson',
                'email': '',
            }),

            ('carte_personne', {
                'nom': 'Laurence Arpin',
                'role': 'Vice-présidente',
                'photo': None,
                'biographie': 'Vétérinaire pour animaux de ferme au Bas-Saint-Laurent et citoyenne engagée pour l\'agriculture biologique et innovante.',
                'email': '',
            }),

            ('carte_personne', {
                'nom': 'Pascal Priori',
                'role': 'Cofondateur',
                'photo': None,
                'biographie': 'Impliqué dans le milieu communautaire au Québec depuis près de 10 ans et spécialisé sur la question des pesticides et leurs impacts sanitaires et environnementaux.',
                'email': '',
            }),

            ('carte_personne', {
                'nom': 'Romain Rigal',
                'role': 'Cofondateur',
                'photo': None,
                'biographie': 'Son expérience professionnelle lui fournit une expertise précieuse dans l\'accompagnement des victimes dans leurs démarches juridiques de reconnaissance.',
                'email': '',
            }),

            ('carte_personne', {
                'nom': 'Monique Bisson',
                'role': 'Cofondatrice',
                'photo': None,
                'biographie': 'Linguiste retraitée, sensible à la question des pesticides et porte-parole de deux membres de sa famille, agriculteur et agricultrice à la retraite atteints de la maladie de Parkinson.',
                'email': '',
            }),

            ('carte_personne', {
                'nom': 'Serge Boily',
                'role': 'Cofondateur',
                'photo': None,
                'biographie': 'Ancien applicateur de pesticides dans le domaine de l\'entretien paysager, atteint de la maladie de Parkinson.',
                'email': '',
            }),

            ('paragraphe', '<p>Tous les membres peuvent poser leur candidature au conseil d\'administration lors de l\'assemblée générale annuelle.</p>'),

            ('titre', 'L\'équipe'),

            ('carte_personne', {
                'nom': 'Amandine François',
                'role': 'Coordinatrice générale',
                'photo': None,
                'biographie': 'Responsable de la coordination générale de VPQ',
                'email': '',
            }),

            ('appel_action', {
                'titre': 'Rejoignez-nous',
                'texte': 'Vous souhaitez soutenir notre cause ou devenir membre ? Contactez-nous dès aujourd\'hui.',
                'lien': '/contact/',
                'texte_bouton': 'Nous contacter',
            }),
        ]

        # Update the page
        apropos.corps = new_blocks
        apropos.save_revision().publish()

        self.stdout.write(self.style.SUCCESS(f'Successfully enhanced page: {apropos.title}'))
        self.stdout.write(self.style.SUCCESS(f'Added {len(new_blocks)} blocks to the page'))
