from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
from wagtail.images.models import Image
from home.models import HomePage
import os


class Command(BaseCommand):
    help = 'Update hero banner with new image'

    def handle(self, *args, **options):
        try:
            # Get the homepage
            homepage = HomePage.objects.first()

            if not homepage:
                self.stdout.write(self.style.ERROR('No HomePage found.'))
                return

            # Import the new hero image
            image_path = 'media/temp_images/hero_banner.webp'

            if not os.path.exists(image_path):
                self.stdout.write(self.style.ERROR(f'Image not found: {image_path}'))
                return

            # Check if image already exists
            hero_image = Image.objects.filter(title='Hero Banner - Champs agricoles').first()

            if not hero_image:
                # Create new image
                with open(image_path, 'rb') as image_file:
                    hero_image = Image(
                        title='Hero Banner - Champs agricoles',
                    )
                    hero_image.file.save(
                        'hero_banner.webp',
                        ImageFile(image_file),
                        save=True
                    )
                    self.stdout.write(self.style.SUCCESS(f'✓ Imported new hero image'))
            else:
                self.stdout.write(self.style.WARNING('Hero image already exists, using existing one'))

            # Update the first hero block with new image
            updated_blocks = []
            hero_updated = False

            for block in homepage.corps:
                if block.block_type == 'hero_block' and not hero_updated:
                    # Update the image_fond field
                    block_dict = dict(block.value)
                    block_dict['image_fond'] = hero_image
                    updated_blocks.append(('hero_block', block_dict))
                    hero_updated = True
                    self.stdout.write(self.style.SUCCESS('✓ Updated hero block with new image'))
                else:
                    # Keep other blocks as-is
                    if hasattr(block.value, '__iter__') and not isinstance(block.value, (str, bytes)):
                        try:
                            updated_blocks.append((block.block_type, dict(block.value)))
                        except:
                            updated_blocks.append((block.block_type, block.value))
                    else:
                        updated_blocks.append((block.block_type, block.value))

            # Save updated blocks
            homepage.corps = updated_blocks
            homepage.save_revision().publish()

            self.stdout.write(self.style.SUCCESS('\n✓ Hero banner successfully updated!'))
            self.stdout.write(self.style.SUCCESS('View at: http://127.0.0.1:8000/'))

        except Exception as exception:
            self.stdout.write(self.style.ERROR(f'Error: {str(exception)}'))
            import traceback
            traceback.print_exc()
            raise
