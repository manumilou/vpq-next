from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
from wagtail.images.models import Image
from home.models import HomePage
import json


class Command(BaseCommand):
    help = 'Populate the homepage with sample hero blocks'

    def handle(self, *args, **options):
        try:
            # Get the homepage
            homepage = HomePage.objects.first()

            if not homepage:
                self.stdout.write(self.style.ERROR('No HomePage found. Please create one first.'))
                return

            self.stdout.write(f'Found homepage: {homepage.title}')

            # Create a placeholder image note for the user
            placeholder_image_id = None

            # Check if there are any images in the system we can use
            existing_image = Image.objects.first()
            if existing_image:
                placeholder_image_id = existing_image.id
                self.stdout.write(self.style.SUCCESS(f'Using existing image: {existing_image.title}'))
            else:
                self.stdout.write(self.style.WARNING('No images found. You will need to add images manually in the admin.'))

            # Create hero blocks data
            hero_blocks = [
                {
                    'type': 'hero_block',
                    'value': {
                        'image_fond': placeholder_image_id,
                        'titre_principal': 'La voix des victimes des pesticides au Québec',
                        'sous_titre': 'Pour une agriculture sans poison',
                        'texte_bouton': 'Découvrir nos actions',
                        'lien_bouton': '#',
                        'opacite_overlay': 45
                    }
                },
                {
                    'type': 'hero_block',
                    'value': {
                        'image_fond': placeholder_image_id,
                        'titre_principal': 'Protéger la santé, défendre l\'environnement',
                        'sous_titre': 'Notre mission est de donner une voix aux victimes et de promouvoir une agriculture durable',
                        'texte_bouton': 'En savoir plus',
                        'lien_bouton': '#',
                        'opacite_overlay': 40
                    }
                },
                {
                    'type': 'hero_block',
                    'value': {
                        'image_fond': placeholder_image_id,
                        'titre_principal': 'Rejoignez le mouvement',
                        'sous_titre': 'Ensemble, nous pouvons faire la différence',
                        'texte_bouton': 'Témoigner',
                        'lien_bouton': '#',
                        'opacite_overlay': 50
                    }
                },
            ]

            # Update the corps field with hero blocks
            # Preserve any existing content that isn't hero blocks
            existing_blocks = []
            if homepage.corps:
                existing_blocks = [block for block in homepage.corps if block.block_type != 'hero_block']

            # Combine hero blocks with existing content
            homepage.corps = hero_blocks + existing_blocks

            # Save the page
            homepage.save_revision().publish()

            self.stdout.write(self.style.SUCCESS('✓ Successfully added hero blocks to homepage!'))
            self.stdout.write(self.style.SUCCESS(f'✓ Added {len(hero_blocks)} hero blocks'))

            if not placeholder_image_id:
                self.stdout.write(self.style.WARNING('\n⚠ IMPORTANT: No images were found in your system.'))
                self.stdout.write(self.style.WARNING('Please upload background images in the Wagtail admin:'))
                self.stdout.write(self.style.WARNING('1. Go to http://127.0.0.1:8000/admin/images/'))
                self.stdout.write(self.style.WARNING('2. Upload crop field photos (1920x1080px recommended)'))
                self.stdout.write(self.style.WARNING('3. Edit the Home page and select proper images for each hero block'))
            else:
                self.stdout.write(self.style.WARNING('\n⚠ Using placeholder image. Please replace with proper crop field photos.'))

            self.stdout.write(self.style.SUCCESS(f'\nView your homepage at: http://127.0.0.1:8000/'))

        except Exception as exception:
            self.stdout.write(self.style.ERROR(f'Error: {str(exception)}'))
            raise
