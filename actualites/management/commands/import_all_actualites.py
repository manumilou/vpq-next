from django.core.management.base import BaseCommand
from datetime import datetime
from actualites.models import ActualiteIndexPage, ActualitePage
from home.models import HomePage


class Command(BaseCommand):
    help = 'Create ActualiteIndexPage and import all news articles from original site'

    def handle(self, *args, **options):
        # Get the homepage
        try:
            homepage = HomePage.objects.get(slug='home')
        except HomePage.DoesNotExist:
            self.stdout.write(self.style.ERROR('HomePage not found'))
            return

        # Create ActualiteIndexPage if it doesn't exist
        try:
            index_page = ActualiteIndexPage.objects.get(slug='actualites')
            self.stdout.write(self.style.WARNING('ActualiteIndexPage already exists'))
        except ActualiteIndexPage.DoesNotExist:
            index_page = ActualiteIndexPage(
                title='Actualités',
                slug='actualites',
                introduction='Suivez nos actualités, communiqués de presse et actions pour la défense des droits des victimes des pesticides au Québec.',
            )
            homepage.add_child(instance=index_page)
            index_page.save_revision().publish()
            self.stdout.write(self.style.SUCCESS('Created ActualiteIndexPage'))

        # News articles data
        articles_data = [
            {
                'title': 'Victimes des pesticides du Québec intègre l\'Association pour la santé publique du Québec',
                'slug': 'alliance-aspq',
                'date': '2025-06-25',
                'introduction': 'Victimes des pesticides du Québec annonce son intégration à l\'Association pour la santé publique du Québec (ASPQ), renforçant ainsi sa capacité d\'action et de représentation.',
                'content': '<p>Après plus de cinq années d\'actions indépendantes, Victimes des pesticides du Québec devient une initiative de l\'Association pour la santé publique du Québec (ASPQ). Cette transition stratégique permettra de consolider nos efforts de défense des droits des victimes et de prévention des risques associés aux pesticides.</p><p>Cette alliance renforce notre capacité à accompagner les victimes dans leurs démarches et à porter nos revendications auprès des instances gouvernementales.</p>',
            },
            {
                'title': 'Reconnaissance des malades liés aux pesticides, victoire de Serge Boily',
                'slug': 'parkinson-cnesst-boily',
                'date': '2025-05-30',
                'introduction': 'Serge Boily obtient la reconnaissance de sa maladie de Parkinson comme maladie professionnelle par la CNESST, marquant une victoire importante pour les victimes des pesticides.',
                'content': '<p>Serge Boily, cofondateur de Victimes des pesticides du Québec et ancien applicateur de pesticides dans le domaine de l\'entretien paysager, vient d\'obtenir la reconnaissance de sa maladie de Parkinson comme maladie professionnelle par la CNESST.</p><p>Cette décision marque une étape importante dans la reconnaissance des droits des travailleurs exposés aux pesticides et confirme le lien entre l\'exposition professionnelle aux pesticides et le développement de la maladie de Parkinson.</p>',
            },
            {
                'title': 'Savoir pour agir - Sondage inédit sur l\'exposition aux pesticides des agriculteurs·trices québécois·es',
                'slug': 'rapport-sondage-2025',
                'date': '2025-02-19',
                'introduction': 'Publication d\'un sondage inédit révélant l\'ampleur de l\'exposition aux pesticides chez les agriculteurs et agricultrices du Québec.',
                'content': '<p>VPQ publie les résultats d\'un sondage inédit mené auprès des agriculteurs et agricultrices du Québec sur leur exposition aux pesticides et les impacts sur leur santé.</p><p>Les résultats révèlent des données préoccupantes sur les niveaux d\'exposition et soulignent l\'urgence d\'agir pour mieux protéger les travailleurs agricoles.</p>',
            },
            {
                'title': 'Deuxième édition de la tournée québécoise de sensibilisation aux pesticides',
                'slug': 'tournee-2023',
                'date': '2023-09-25',
                'introduction': 'VPQ lance la deuxième édition de sa tournée de sensibilisation aux risques des pesticides à travers le Québec.',
                'content': '<p>Victimes des pesticides du Québec annonce la deuxième édition de sa tournée de sensibilisation aux risques des pesticides à travers différentes régions du Québec.</p><p>Cette tournée vise à informer le public, les travailleurs et les décideurs sur les impacts sanitaires des pesticides et à promouvoir des alternatives non toxiques.</p>',
            },
            {
                'title': 'Appel aux dons pour le combat de Jean-François',
                'slug': 'appel-dons',
                'date': '2023-07-17',
                'introduction': 'Lancement d\'un appel aux dons pour soutenir Jean-François dans sa lutte pour la reconnaissance de sa maladie professionnelle.',
                'content': '<p>VPQ lance un appel aux dons pour soutenir Jean-François dans son combat pour obtenir la reconnaissance de sa maladie comme maladie professionnelle liée à l\'exposition aux pesticides.</p><p>Les frais juridiques et médicaux représentent un fardeau important pour les victimes. Votre soutien fait une différence.</p>',
            },
            {
                'title': 'Des changements superficiels proposés par Santé-Canada',
                'slug': 'reaction-annonce',
                'date': '2023-06-21',
                'introduction': 'VPQ réagit aux propositions de Santé Canada concernant la révision du cadre d\'autorisation des pesticides.',
                'content': '<p>Victimes des pesticides du Québec déplore les changements superficiels proposés par Santé Canada dans la révision du cadre d\'autorisation des pesticides au Canada.</p><p>Nous demandons des mesures beaucoup plus ambitieuses pour protéger la santé des Canadiens et Canadiennes face aux risques des pesticides.</p>',
            },
            {
                'title': 'Retour sur la mission en France, fonds d\'indemnisation des victimes des pesticides',
                'slug': 'mission-france',
                'date': '2023-05-04',
                'introduction': 'Compte-rendu de la mission en France pour étudier le fonds d\'indemnisation des victimes des pesticides.',
                'content': '<p>Une délégation de VPQ s\'est rendue en France pour rencontrer les acteurs du fonds d\'indemnisation des victimes des pesticides et étudier la possibilité de mettre en place un système similaire au Québec.</p><p>Cette mission a permis de mieux comprendre les mécanismes de reconnaissance et d\'indemnisation en place en France depuis plusieurs années.</p>',
            },
            {
                'title': 'Dépôt de la pétition contre le glyphosate, des mesures urgentes demandées par une coalition de Canadien.ne.s',
                'slug': 'petition-glyphosate',
                'date': '2023-05-01',
                'introduction': 'Dépôt d\'une pétition demandant des mesures urgentes contre l\'utilisation du glyphosate au Canada.',
                'content': '<p>Une coalition d\'organisations canadiennes, dont VPQ, dépose une pétition demandant au gouvernement fédéral de prendre des mesures urgentes pour encadrer et réduire l\'utilisation du glyphosate.</p><p>Des milliers de Canadiens et Canadiennes ont signé cette pétition pour demander une meilleure protection de leur santé et de l\'environnement.</p>',
            },
            {
                'title': 'En cas d\'utilisation de pesticides, protégez-vous !',
                'slug': 'epi',
                'date': '2023-04-21',
                'introduction': 'Rappel des mesures de protection essentielles lors de l\'utilisation de pesticides.',
                'content': '<p>VPQ publie un guide des équipements de protection individuelle (ÉPI) essentiels pour les personnes amenées à manipuler des pesticides.</p><p>Une protection adéquate est cruciale pour réduire les risques d\'exposition et protéger sa santé. Consultez nos recommandations.</p>',
            },
            {
                'title': 'Action devant l\'Assemblée nationale du Québec',
                'slug': 'action-qc',
                'date': '2023-04-03',
                'introduction': 'VPQ organise une action de sensibilisation devant l\'Assemblée nationale pour réclamer de meilleures protections.',
                'content': '<p>Des membres et sympathisants de VPQ se sont rassemblés devant l\'Assemblée nationale du Québec pour demander au gouvernement d\'agir pour mieux protéger la population contre les risques des pesticides.</p><p>Cette action visait à sensibiliser les élus à l\'urgence de la situation et à la nécessité de renforcer la réglementation.</p>',
            },
            {
                'title': 'Épisode de la Semaine verte, l\'héritage des pesticides',
                'slug': 'semaine-verte',
                'date': '2023-03-20',
                'introduction': 'VPQ participe à un épisode de l\'émission La Semaine verte consacré aux impacts des pesticides.',
                'content': '<p>Des membres de VPQ témoignent dans un épisode de l\'émission La Semaine verte diffusée sur Radio-Canada, abordant l\'héritage toxique des pesticides sur la santé des travailleurs agricoles.</p><p>Cet épisode met en lumière les histoires des victimes et les enjeux de santé publique liés à l\'utilisation des pesticides.</p>',
            },
            {
                'title': 'Invitation à l\'assemblée générale annuelle de VPQ',
                'slug': 'aga-2023',
                'date': '2023-03-15',
                'introduction': 'Invitation à l\'assemblée générale annuelle 2023 de Victimes des pesticides du Québec.',
                'content': '<p>Tous les membres de VPQ sont invités à participer à l\'assemblée générale annuelle qui se tiendra en mars 2023.</p><p>Cette rencontre sera l\'occasion de faire le bilan de nos actions, d\'élire le conseil d\'administration et de planifier les orientations futures de l\'organisation.</p>',
            },
            {
                'title': 'Un malade de parkinson reconnu par la CNESST',
                'slug': 'premiere_reconnaissance',
                'date': '2022-11-08',
                'introduction': 'Première reconnaissance d\'un cas de maladie de Parkinson comme maladie professionnelle par la CNESST.',
                'content': '<p>Pour la première fois, la CNESST reconnaît un cas de maladie de Parkinson comme maladie professionnelle liée à l\'exposition aux pesticides.</p><p>Cette décision historique ouvre la voie à d\'autres victimes pour obtenir reconnaissance et indemnisation pour leur maladie.</p>',
            },
            {
                'title': 'Des actions urgentes sont à prendre pour réviser le cadre d\'autorisation des pesticides au Canada',
                'slug': 'memoire-arla',
                'date': '2022-07-02',
                'introduction': 'VPQ présente un mémoire à l\'ARLA demandant une révision en profondeur du cadre d\'autorisation des pesticides.',
                'content': '<p>Victimes des pesticides du Québec dépose un mémoire détaillé à l\'Agence de réglementation de la lutte antiparasitaire (ARLA) demandant des actions urgentes pour réviser le cadre d\'autorisation des pesticides au Canada.</p><p>Notre mémoire souligne les lacunes du système actuel et propose des recommandations concrètes pour mieux protéger la santé de la population.</p>',
            },
            {
                'title': 'Tournée québécoise de sensibilisation aux pesticides',
                'slug': 'tournee2022',
                'date': '2022-03-04',
                'introduction': 'Lancement de la première tournée de sensibilisation de VPQ à travers le Québec.',
                'content': '<p>VPQ lance sa première tournée de sensibilisation aux pesticides à travers différentes régions du Québec pour rencontrer les citoyens, les travailleurs agricoles et les décideurs locaux.</p><p>Cette tournée vise à informer sur les risques des pesticides et à promouvoir des alternatives plus saines pour l\'agriculture et l\'environnement.</p>',
            },
            {
                'title': 'La maladie de Parkinson reconnue comme maladie professionnelle',
                'slug': 'reconnaissanceparkinson',
                'date': '2021-12-07',
                'introduction': 'Victoire historique : la maladie de Parkinson est désormais reconnue comme maladie professionnelle au Québec.',
                'content': '<p>Après des mois de mobilisation, le gouvernement du Québec reconnaît officiellement la maladie de Parkinson comme maladie professionnelle pour les travailleurs exposés aux pesticides.</p><p>Cette reconnaissance, obtenue grâce au travail conjoint de VPQ et Parkinson Québec, est une première en Amérique du Nord et représente une victoire majeure pour les victimes des pesticides.</p>',
            },
            {
                'title': 'Victimes des pesticides du Québec recrute!',
                'slug': 'offrecoordo',
                'date': '2021-07-30',
                'introduction': 'VPQ est à la recherche d\'un ou d\'une coordinatrice générale pour rejoindre l\'équipe.',
                'content': '<p>Victimes des pesticides du Québec recrute un ou une coordinatrice générale pour accompagner le développement de l\'organisation et coordonner nos actions de défense des droits des victimes.</p><p>Consultez l\'offre d\'emploi complète sur notre site.</p>',
            },
            {
                'title': 'Reconnaissance de la maladie de Parkinson comme maladie professionnelle, une première étape indispensable',
                'slug': 'reconnaissance-parkinson',
                'date': '2021-03-30',
                'introduction': 'VPQ salue les avancées vers la reconnaissance de la maladie de Parkinson comme maladie professionnelle.',
                'content': '<p>Victimes des pesticides du Québec et Parkinson Québec saluent les avancées du projet de loi modernisant le régime de santé et sécurité au travail, qui ouvre la voie à la reconnaissance de la maladie de Parkinson comme maladie professionnelle.</p><p>Cette première étape est indispensable mais devra être suivie de mesures concrètes pour faciliter l\'accès à la reconnaissance et à l\'indemnisation.</p>',
            },
            {
                'title': 'Mémoire de Victimes des pesticides du Québec et Parkinson Québec',
                'slug': 'memoire-sst-projet-loi-59',
                'date': '2021-01-19',
                'introduction': 'VPQ et Parkinson Québec déposent un mémoire conjoint sur le projet de loi 59 concernant la santé et sécurité au travail.',
                'content': '<p>Victimes des pesticides du Québec et Parkinson Québec présentent un mémoire conjoint dans le cadre des consultations sur le projet de loi 59 visant à moderniser le régime de santé et sécurité au travail.</p><p>Ce mémoire demande la reconnaissance explicite de la maladie de Parkinson comme maladie professionnelle pour les travailleurs exposés aux pesticides.</p>',
            },
            {
                'title': 'Les agriculteurs, grands exclus du projet de modernisation du régime de santé et de sécurité du travail',
                'slug': 'loi-sante-securite-travail',
                'date': '2020-10-27',
                'introduction': 'VPQ dénonce l\'exclusion des agriculteurs du projet de modernisation de la loi sur la santé et sécurité au travail.',
                'content': '<p>Victimes des pesticides du Québec déplore que les travailleurs agricoles demeurent les grands exclus du projet de modernisation du régime de santé et sécurité au travail.</p><p>Pourtant particulièrement exposés aux pesticides, ces travailleurs méritent une meilleure protection et un accès facilité à la reconnaissance des maladies professionnelles.</p>',
            },
            {
                'title': 'Un nouveau plan en agriculture à la hauteur des enjeux?',
                'slug': 'plan-agriculture-durable',
                'date': '2020-10-23',
                'introduction': 'Analyse du nouveau plan gouvernemental en agriculture durable et ses implications pour la réduction des pesticides.',
                'content': '<p>VPQ analyse le nouveau plan en agriculture durable annoncé par le gouvernement du Québec et questionne si les mesures proposées sont véritablement à la hauteur des enjeux sanitaires et environnementaux.</p><p>Nous demandons des cibles chiffrées de réduction de l\'utilisation des pesticides et des investissements significatifs dans les alternatives non toxiques.</p>',
            },
            {
                'title': 'Création d\'une nouvelle organisation pour défendre les droits des personnes exposées aux pesticides',
                'slug': 'lancement-site-vpq',
                'date': '2020-09-26',
                'introduction': 'Lancement officiel de Victimes des pesticides du Québec, organisation dédiée à la défense des droits des victimes.',
                'content': '<p>Victimes des pesticides du Québec annonce officiellement son lancement et la mise en ligne de son site web.</p><p>Cette nouvelle organisation a pour mission de défendre les droits des personnes exposées aux pesticides, de les accompagner dans leurs démarches et de sensibiliser le public aux risques sanitaires associés aux pesticides.</p><p>Fondée en décembre 2019, VPQ regroupe des victimes, des associations de patients et des citoyens engagés pour un Québec en santé.</p>',
            },
        ]

        # Import all articles
        imported_count = 0
        for article_data in articles_data:
            # Check if article already exists
            if ActualitePage.objects.filter(slug=article_data['slug']).exists():
                self.stdout.write(self.style.WARNING(f'Article "{article_data["title"]}" already exists, skipping'))
                continue

            # Parse date
            date_pub = datetime.strptime(article_data['date'], '%Y-%m-%d').date()

            # Create article
            article = ActualitePage(
                title=article_data['title'],
                slug=article_data['slug'],
                date_publication=date_pub,
                introduction=article_data['introduction'],
                corps=[('paragraphe', article_data['content'])],
            )

            index_page.add_child(instance=article)
            article.save_revision().publish()
            imported_count += 1

            self.stdout.write(self.style.SUCCESS(f'Imported: {article.title}'))

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully imported {imported_count} news articles'))
        self.stdout.write(self.style.SUCCESS(f'ActualiteIndexPage URL: /actualites/'))
