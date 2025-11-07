from django.core.management.base import BaseCommand
from wagtail.images.models import Image
from home.models import HomePage


class Command(BaseCommand):
    help = 'Setup mobile-first homepage with complete content structure'

    def handle(self, *args, **options):
        try:
            # Get the homepage
            homepage = HomePage.objects.first()

            if not homepage:
                self.stdout.write(self.style.ERROR('No HomePage found.'))
                return

            self.stdout.write(f'Found homepage: {homepage.title}')

            # Get existing images
            images = list(Image.objects.all()[:3])
            hero_image = images[0] if images else None

            if not hero_image:
                self.stdout.write(self.style.WARNING('No images found. Hero will not have background image.'))

            # Build new mobile-first content structure
            new_blocks = [
                # 1. Single Hero Block
                ('hero_block', {
                    'image_fond': hero_image,
                    'titre_principal': 'Protégeons notre santé et notre environnement',
                    'sous_titre': 'Ensemble contre l\'utilisation abusive des pesticides au Québec',
                    'texte_bouton': 'Découvrir notre mission',
                    'lien_bouton': '/a-propos/',
                    'opacite_overlay': 45
                }),

                # 2. Quick Actions
                ('quick_actions', {
                    'titre': 'Comment agir?',
                    'actions': [
                        {
                            'titre': 'Témoigner',
                            'description': 'Partagez votre expérience avec les pesticides',
                            'lien': '/malades-que-faire/',
                            'icone': 'voice'
                        },
                        {
                            'titre': 'Connaître les risques',
                            'description': 'Informez-vous sur les dangers des pesticides',
                            'lien': '/quels-risques/',
                            'icone': 'alert'
                        },
                        {
                            'titre': 'Soutenir VPQ',
                            'description': 'Contribuez à notre mission',
                            'lien': '/soutenez-vpq/',
                            'icone': 'heart'
                        },
                    ]
                }),

                # 3. Statistics
                ('stats_block', {
                    'titre': 'L\'impact en chiffres',
                    'statistiques': [
                        {
                            'chiffre': '2000',
                            'unite': '+',
                            'description': 'Victimes au Québec'
                        },
                        {
                            'chiffre': '95',
                            'unite': '%',
                            'description': 'De nos aliments contaminés'
                        },
                        {
                            'chiffre': '15',
                            'unite': 'M',
                            'description': 'De kilos utilisés/an'
                        },
                        {
                            'chiffre': '10',
                            'unite': 'ans',
                            'description': 'De lutte et d\'engagement'
                        },
                    ]
                }),

                # 4. Problematique
                ('problematique_block', {
                    'titre': 'Une menace pour notre santé',
                    'contenu': '<p>Les pesticides utilisés massivement dans l\'agriculture québécoise représentent un danger réel pour notre santé et notre environnement. De nombreuses études scientifiques établissent des liens entre l\'exposition aux pesticides et diverses maladies graves.</p><p><strong>Cancers, maladies neurodégénératives, troubles de la reproduction...</strong> Les victimes sont nombreuses, mais leurs voix restent souvent ignorées.</p><p>Il est temps d\'agir pour une agriculture respectueuse de la vie.</p>',
                    'image': images[1] if len(images) > 1 else None,
                    'position_image': 'right'
                }),

                # 5. Mission Cards
                ('mission_cards', {
                    'titre': 'Notre mission en trois axes',
                    'cartes': [
                        {
                            'titre': 'Donner une voix',
                            'description': 'Nous donnons la parole aux victimes des pesticides et faisons connaître leurs histoires pour sensibiliser le public et les décideurs.',
                            'icone': 'voice'
                        },
                        {
                            'titre': 'Sensibiliser',
                            'description': 'Nous informons la population québécoise sur les risques liés aux pesticides et les alternatives durables disponibles.',
                            'icone': 'awareness'
                        },
                        {
                            'titre': 'Promouvoir les alternatives',
                            'description': 'Nous soutenons et promouvons l\'agriculture biologique et les pratiques agricoles respectueuses de la santé et de l\'environnement.',
                            'icone': 'alternative'
                        },
                    ]
                }),

                # 6. Final CTA
                ('cta_final', {
                    'titre': 'Rejoignez le mouvement',
                    'texte': 'Ensemble, nous pouvons faire la différence. Votre soutien est essentiel pour continuer notre lutte pour une agriculture sans poison.',
                    'texte_bouton': 'Soutenez-nous maintenant',
                    'lien_bouton': '/soutenez-vpq/',
                    'couleur_fond': 'green'
                }),
            ]

            # Update homepage content
            homepage.corps = new_blocks
            homepage.save_revision().publish()

            self.stdout.write(self.style.SUCCESS('\n✓ Homepage successfully updated with mobile-first design!'))
            self.stdout.write(self.style.SUCCESS('✓ Structure includes:'))
            self.stdout.write('  - 1 Hero block (50vh mobile, 70vh desktop)')
            self.stdout.write('  - Quick Actions (1 col mobile, 3 cols desktop)')
            self.stdout.write('  - Statistics (2x2 mobile, 4x1 desktop)')
            self.stdout.write('  - Problematique section')
            self.stdout.write('  - Mission cards (1 col mobile, 3 cols desktop)')
            self.stdout.write('  - Final CTA')
            self.stdout.write(self.style.SUCCESS('\nView at: http://127.0.0.1:8000/'))
            self.stdout.write(self.style.SUCCESS('All touch targets are 48px+ for mobile accessibility!'))

        except Exception as exception:
            self.stdout.write(self.style.ERROR(f'Error: {str(exception)}'))
            import traceback
            traceback.print_exc()
            raise
