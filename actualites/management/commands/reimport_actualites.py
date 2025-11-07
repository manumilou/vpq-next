from django.core.management.base import BaseCommand
from datetime import datetime
from actualites.models import ActualiteIndexPage, ActualitePage
from home.models import HomePage


class Command(BaseCommand):
    help = 'Re-import news articles - first 5 with full content, rest with basic info'

    def handle(self, *args, **options):
        # Get the ActualiteIndexPage
        try:
            index_page = ActualiteIndexPage.objects.get(slug='actualites')
        except ActualiteIndexPage.DoesNotExist:
            self.stdout.write(self.style.ERROR('ActualiteIndexPage not found'))
            return

        # Top 5 articles with REAL full content
        top_5_articles = [
            {
                'title': 'Victimes des pesticides du Québec intègre l\'Association pour la santé publique du Québec',
                'slug': 'alliance-aspq',
                'date': '2025-06-25',
                'introduction': 'Le 25 juin 2025, Victimes des pesticides du Québec (VPQ) annonce son intégration à l\'Association pour la santé publique du Québec (ASPQ), renforçant ainsi sa capacité d\'action.',
                'content': '<p>Victimes des pesticides du Québec (VPQ) représente les personnes affectées par l\'exposition aux pesticides, ainsi que des experts et des groupes de défense des patients. L\'organisation œuvre pour défendre les droits des personnes touchées par des maladies liées aux pesticides et prévenir les risques sanitaires associés, particulièrement en agriculture.</p><p>Thomas Bastien, directeur général de l\'ASPQ, a déclaré : « En accueillant VPQ, nous gagnons une expertise citoyenne précieuse et renforçons notre engagement envers la prévention des maladies évitables. »</p><p>Serge Boily, président de VPQ, a expliqué la valeur stratégique : « Rejoindre l\'ASPQ nous permet de bénéficier d\'une expertise reconnue et d\'accroître la sensibilisation aux impacts réels des pesticides sur la santé. »</p><p>Parmi les priorités clés figurent l\'ajout du lymphome non hodgkinien, du myélome multiple et du cancer de la prostate aux listes des maladies professionnelles, ainsi que l\'établissement d\'un fonds d\'indemnisation pour les travailleurs non couverts par la CNESST.</p><p><strong>Contact :</strong> Véra Ferret, Relations publiques ASPQ (450-626-8879, vferret@aspq.org)</p>',
            },
            {
                'title': 'Reconnaissance des malades liés aux pesticides, victoire de Serge Boily',
                'slug': 'parkinson-cnesst-boily',
                'date': '2025-05-30',
                'introduction': 'Victimes des pesticides du Québec annonce la reconnaissance finale de la maladie de Parkinson comme maladie professionnelle pour Serge Boily, président de l\'organisation.',
                'content': '<p>Cette étape importante s\'est produite lors de l\'événement inaugural Parkinson IQ + You du Canada, créé par la Fondation Michael J. Fox.</p><h3>Le cas de Boily : Un témoignage de persévérance</h3><p>Avec le soutien de VPQ et l\'expertise de l\'avocate Sophie Mongeon, Boily a obtenu une cote d\'atteinte permanente de 375%, une indemnité forfaitaire et un remplacement du revenu jusqu\'à l\'âge de 68 ans. Malgré l\'ajout de la maladie de Parkinson à la liste des maladies professionnelles présumées du Québec en 2021, son cas—initié en novembre 2019—a pris plus de cinq ans à résoudre, rencontrant :</p><ul><li>Déni médical du lien pesticide-maladie</li><li>Rejet initial de l\'indemnisation</li><li>Quatre changements d\'agents de dossier</li><li>Expertises non qualifiées</li><li>Plus de 60 mois de délais</li></ul><h3>Message aux travailleurs touchés</h3><p>Boily a souligné les iniquités systémiques : « Des situations identiques reçoivent des résultats très différents. Les indemnisations gelées depuis plus de 40 ans ne reflètent pas les coûts actuels des traitements. »</p><p>Pascal Priori, cofondateur de VPQ, a insisté sur l\'urgence : « Il semble s\'agir du premier cas de Parkinson entièrement indemnisé via la CNESST malgré des preuves scientifiques abondantes. »</p><h3>Plaidoyer futur</h3><p>VPQ demande la reconnaissance de maladies supplémentaires—myélome multiple, cancer de la prostate, lymphome non hodgkinien et troubles cognitifs—ainsi qu\'un financement pour le soutien aux victimes.</p>',
            },
            {
                'title': 'Savoir pour agir - Sondage inédit sur l\'exposition aux pesticides des agriculteurs·trices québécois·es',
                'slug': 'rapport-sondage-2025',
                'date': '2025-02-19',
                'introduction': 'Un sondage inédit révèle des préoccupations importantes en matière de santé et de sécurité chez les travailleurs agricoles du Québec concernant l\'exposition aux pesticides.',
                'content': '<p>Le 19 février 2025, Victimes des pesticides du Québec a présenté les résultats d\'un sondage mené auprès de 1 465 producteurs agricoles qui ont répondu entre mars et mai 2023. L\'organisation affirme : « il est urgent d\'agir pour protéger tous les travailleurs agricoles du Québec » face aux maladies liées aux pesticides.</p><h3>Principales préoccupations identifiées</h3><p><strong>Inquiétudes sanitaires :</strong> Environ 1 répondant sur 8 (12,7%) a déclaré souffrir de conditions ayant des liens forts, modérés ou faibles avec l\'utilisation de pesticides.</p><p><strong>Exposition infantile :</strong> Plus d\'un tiers (39,7%) ont été exposés aux pesticides pendant l\'enfance ou l\'adolescence, tandis qu\'environ 1 agricultrice sur 5 (18,9%) a déclaré une exposition pendant la grossesse.</p><p><strong>Contamination au travail :</strong> 196 personnes ont rapporté avoir travaillé dans des champs avant la fin des délais de réentrée sécuritaire après l\'application de pesticides.</p><p><strong>Crise de sous-déclaration :</strong> Un alarmant 97,6% des empoisonnements aigus n\'ont pas été signalés aux autorités sanitaires. Parmi 307 personnes présentant des symptômes légers d\'empoisonnement, seulement 2,3% ont déposé un rapport.</p><p><strong>Protection inadéquate :</strong> Environ 1 travailleur sur 5 portait rarement ou jamais d\'équipement de protection lors de l\'exposition aux pesticides.</p><p><strong>Lacunes en assurance :</strong> Près de 69% ne disposent pas de couverture d\'indemnisation des travailleurs, et 37% n\'ont ni assurance maladie privée ni protection CNESST.</p>',
            },
            {
                'title': 'Deuxième édition de la tournée québécoise de sensibilisation aux pesticides',
                'slug': 'tournee-2023',
                'date': '2023-09-25',
                'introduction': 'Victimes des pesticides du Québec organise sa deuxième tournée de sensibilisation pour éduquer le public sur les risques des pesticides.',
                'content': '<p>Victimes des pesticides du Québec organise sa deuxième tournée de sensibilisation pour éduquer le public sur les risques des pesticides, partager les expériences des victimes et favoriser un dialogue constructif sur la prévention des préjudices liés aux pesticides.</p><h3>Dates et lieux de la tournée</h3><p>La tournée couvre six villes du Québec en octobre :</p><ul><li><strong>Coteau-du-Lac</strong> (16 octobre, 18h30) – Pavillon Wilson</li><li><strong>Gatineau</strong> (18 octobre, 19h) – La Cabane en bois rond</li><li><strong>Victoriaville</strong> (19 octobre, 18h) – Cégep de Victoriaville Grand Auditorium</li><li><strong>Trois-Rivières</strong> (23 octobre, 19h) – 1060 rue Saint-François-Xavier, Salle 116</li><li><strong>Montréal</strong> (24 octobre, 18h30) – UQAM, Pavillon Kennedy, Salle pk-1140</li><li><strong>Québec</strong> (25 octobre, 19h) – Centre culture et environnement Frédéric Back</li></ul><p>Tous les événements sont gratuits et comprennent la projection de l\'épisode de Radio-Canada « L\'héritage des pesticides » suivie de tables rondes avec des agriculteurs, scientifiques, avocats et représentants d\'organismes de défense.</p><h3>Enjeux clés</h3><p>Bien que le Québec ait reconnu la maladie de Parkinson comme maladie professionnelle liée aux pesticides en 2021, seulement une vingtaine de cas ont reçu l\'approbation de la CNESST. Les critères d\'admissibilité demeurent restrictifs. L\'organisation plaide pour l\'ajout du myélome multiple, du cancer de la prostate, du lymphome non hodgkinien et des troubles cognitifs à la liste des maladies professionnelles.</p><p>L\'organisation souligne le pouvoir de lobbying de l\'industrie tout en opérant sans financement gouvernemental.</p>',
            },
            {
                'title': 'Appel aux dons pour le combat de Jean-François',
                'slug': 'appel-dons',
                'date': '2023-07-17',
                'introduction': 'Campagne de financement pour Jean-François Perichon, 76 ans, ancien paysagiste ayant développé la maladie de Parkinson après plus de deux décennies d\'exposition aux pesticides.',
                'content': '<h3>La situation</h3><p>Jean-François Perichon, 76 ans, ancien paysagiste, a développé la maladie de Parkinson après plus de deux décennies d\'exposition aux pesticides. Perichon remplissait tous les critères d\'admissibilité pour l\'indemnisation des travailleurs par la CNESST du Québec, mais sa demande a été rejetée. Il nécessite maintenant une représentation juridique pour contester cette décision.</p><h3>Le besoin</h3><p>En tant que retraité aux revenus limités, Perichon ne peut pas se permettre les frais juridiques spécialisés nécessaires pour contester le rejet de la CNESST.</p><h3>La campagne</h3><p>L\'organisation « Victimes des pesticides du Québec » recueille des fonds avec un objectif initial de 1 000 $. Ils s\'engagent à ce que les dons soutiennent les batailles juridiques des victimes de pesticides, les fonds excédentaires pouvant potentiellement aider d\'autres personnes.</p><h3>Précédent de succès</h3><p>L\'organisation fait référence à une victoire antérieure—Serge Boily, cofondateur, a été reconnu comme victime d\'une maladie professionnelle en novembre 2022 grâce à leurs efforts collaboratifs avec un conseiller juridique.</p><h3>Appel à l\'action</h3><p>La campagne invite aux dons mensuels à partir de 10-20 $ et encourage les sympathisants à partager le message. Un témoignage vidéo de Perichon est disponible sur YouTube.</p><p><strong>Ensemble, nous ferons la différence !</strong></p>',
            },
        ]

        # Remaining 17 articles with basic info only
        remaining_articles = [
            {
                'title': 'Des changements superficiels proposés par Santé-Canada',
                'slug': 'reaction-annonce',
                'date': '2023-06-21',
                'introduction': 'VPQ réagit aux propositions de Santé Canada concernant la révision du cadre d\'autorisation des pesticides, les jugeant insuffisantes.',
            },
            {
                'title': 'Retour sur la mission en France, fonds d\'indemnisation des victimes des pesticides',
                'slug': 'mission-france',
                'date': '2023-05-04',
                'introduction': 'Compte-rendu de la mission en France pour étudier le fonds d\'indemnisation des victimes des pesticides et explorer la possibilité d\'un système similaire au Québec.',
            },
            {
                'title': 'Dépôt de la pétition contre le glyphosate, des mesures urgentes demandées par une coalition de Canadien.ne.s',
                'slug': 'petition-glyphosate',
                'date': '2023-05-01',
                'introduction': 'Une coalition d\'organisations canadiennes, dont VPQ, dépose une pétition demandant des mesures urgentes pour encadrer et réduire l\'utilisation du glyphosate.',
            },
            {
                'title': 'En cas d\'utilisation de pesticides, protégez-vous !',
                'slug': 'epi',
                'date': '2023-04-21',
                'introduction': 'VPQ publie un guide des équipements de protection individuelle (ÉPI) essentiels pour les personnes amenées à manipuler des pesticides.',
            },
            {
                'title': 'Action devant l\'Assemblée nationale du Québec',
                'slug': 'action-qc',
                'date': '2023-04-03',
                'introduction': 'Des membres et sympathisants de VPQ se sont rassemblés devant l\'Assemblée nationale pour demander au gouvernement d\'agir pour mieux protéger la population.',
            },
            {
                'title': 'Épisode de la Semaine verte, l\'héritage des pesticides',
                'slug': 'semaine-verte',
                'date': '2023-03-20',
                'introduction': 'Des membres de VPQ témoignent dans un épisode de l\'émission La Semaine verte de Radio-Canada, abordant l\'héritage toxique des pesticides.',
            },
            {
                'title': 'Invitation à l\'assemblée générale annuelle de VPQ',
                'slug': 'aga-2023',
                'date': '2023-03-15',
                'introduction': 'Invitation à l\'assemblée générale annuelle 2023 de Victimes des pesticides du Québec pour faire le bilan et planifier les orientations futures.',
            },
            {
                'title': 'Un malade de parkinson reconnu par la CNESST',
                'slug': 'premiere_reconnaissance',
                'date': '2022-11-08',
                'introduction': 'Pour la première fois, la CNESST reconnaît un cas de maladie de Parkinson comme maladie professionnelle liée à l\'exposition aux pesticides.',
            },
            {
                'title': 'Des actions urgentes sont à prendre pour réviser le cadre d\'autorisation des pesticides au Canada',
                'slug': 'memoire-arla',
                'date': '2022-07-02',
                'introduction': 'VPQ dépose un mémoire à l\'ARLA demandant une révision en profondeur du cadre d\'autorisation des pesticides et proposant des recommandations concrètes.',
            },
            {
                'title': 'Tournée québécoise de sensibilisation aux pesticides',
                'slug': 'tournee2022',
                'date': '2022-03-04',
                'introduction': 'VPQ lance sa première tournée de sensibilisation aux pesticides à travers différentes régions du Québec pour informer sur les risques et promouvoir des alternatives.',
            },
            {
                'title': 'La maladie de Parkinson reconnue comme maladie professionnelle',
                'slug': 'reconnaissanceparkinson',
                'date': '2021-12-07',
                'introduction': 'Victoire historique : le gouvernement du Québec reconnaît officiellement la maladie de Parkinson comme maladie professionnelle pour les travailleurs exposés aux pesticides.',
            },
            {
                'title': 'Victimes des pesticides du Québec recrute!',
                'slug': 'offrecoordo',
                'date': '2021-07-30',
                'introduction': 'VPQ est à la recherche d\'un ou d\'une coordinatrice générale pour accompagner le développement de l\'organisation et coordonner nos actions.',
            },
            {
                'title': 'Reconnaissance de la maladie de Parkinson comme maladie professionnelle, une première étape indispensable',
                'slug': 'reconnaissance-parkinson',
                'date': '2021-03-30',
                'introduction': 'VPQ et Parkinson Québec saluent les avancées du projet de loi modernisant le régime de santé et sécurité au travail.',
            },
            {
                'title': 'Mémoire de Victimes des pesticides du Québec et Parkinson Québec',
                'slug': 'memoire-sst-projet-loi-59',
                'date': '2021-01-19',
                'introduction': 'VPQ et Parkinson Québec présentent un mémoire conjoint sur le projet de loi 59 demandant la reconnaissance de la maladie de Parkinson comme maladie professionnelle.',
            },
            {
                'title': 'Les agriculteurs, grands exclus du projet de modernisation du régime de santé et de sécurité du travail',
                'slug': 'loi-sante-securite-travail',
                'date': '2020-10-27',
                'introduction': 'VPQ déplore que les travailleurs agricoles demeurent les grands exclus du projet de modernisation du régime de santé et sécurité au travail.',
            },
            {
                'title': 'Un nouveau plan en agriculture à la hauteur des enjeux?',
                'slug': 'plan-agriculture-durable',
                'date': '2020-10-23',
                'introduction': 'VPQ analyse le nouveau plan en agriculture durable et questionne si les mesures proposées sont véritablement à la hauteur des enjeux sanitaires.',
            },
            {
                'title': 'Création d\'une nouvelle organisation pour défendre les droits des personnes exposées aux pesticides',
                'slug': 'lancement-site-vpq',
                'date': '2020-09-26',
                'introduction': 'Lancement officiel de Victimes des pesticides du Québec, organisation dédiée à la défense des droits des victimes et à la sensibilisation aux risques des pesticides.',
            },
        ]

        # Import top 5 with full content
        imported_full = 0
        for article_data in top_5_articles:
            if ActualitePage.objects.filter(slug=article_data['slug']).exists():
                self.stdout.write(self.style.WARNING(f'Article "{article_data["title"]}" already exists'))
                continue

            date_pub = datetime.strptime(article_data['date'], '%Y-%m-%d').date()
            article = ActualitePage(
                title=article_data['title'],
                slug=article_data['slug'],
                date_publication=date_pub,
                introduction=article_data['introduction'],
                corps=[('paragraphe', article_data['content'])],
            )
            index_page.add_child(instance=article)
            article.save_revision().publish()
            imported_full += 1
            self.stdout.write(self.style.SUCCESS(f'Imported (FULL): {article.title}'))

        # Import remaining 17 with basic info
        imported_basic = 0
        for article_data in remaining_articles:
            if ActualitePage.objects.filter(slug=article_data['slug']).exists():
                self.stdout.write(self.style.WARNING(f'Article "{article_data["title"]}" already exists'))
                continue

            date_pub = datetime.strptime(article_data['date'], '%Y-%m-%d').date()
            article = ActualitePage(
                title=article_data['title'],
                slug=article_data['slug'],
                date_publication=date_pub,
                introduction=article_data['introduction'],
                corps=[],  # Empty content for now
            )
            index_page.add_child(instance=article)
            article.save_revision().publish()
            imported_basic += 1
            self.stdout.write(self.style.SUCCESS(f'Imported (basic): {article.title}'))

        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully imported {imported_full} articles with full content'))
        self.stdout.write(self.style.SUCCESS(f'✅ Successfully imported {imported_basic} articles with basic info'))
        self.stdout.write(self.style.SUCCESS(f'📰 Total: {imported_full + imported_basic} articles'))
        self.stdout.write(self.style.SUCCESS(f'🔗 ActualiteIndexPage URL: /actualites/'))
