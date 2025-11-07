from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
from wagtail.images.models import Image
from home.models import HomePage
import os


class Command(BaseCommand):
    help = 'Import hero images and update homepage hero blocks'

    def handle(self, *args, **options):
        try:
            # Get the homepage
            homepage = HomePage.objects.first()

            if not homepage:
                self.stdout.write(self.style.ERROR('No HomePage found.'))
                return

            self.stdout.write(f'Found homepage: {homepage.title}')

            # Define images to import
            images_data = [
                {
                    'path': 'media/temp_images/crop_field_1.jpg',
                    'title': 'Champ de cultures - Paysage agricole',
                    'description': 'Large crop field with agricultural landscape'
                },
                {
                    'path': 'media/temp_images/crop_field_2.jpg',
                    'title': 'Agriculture durable - Terres cultivées',
                    'description': 'Sustainable agriculture farmland'
                },
                {
                    'path': 'media/temp_images/crop_field_3.jpg',
                    'title': 'Champs du Québec - Agriculture',
                    'description': 'Quebec agricultural fields'
                },
            ]

            imported_images = []

            # Import images into Wagtail
            for img_data in images_data:
                if not os.path.exists(img_data['path']):
                    self.stdout.write(self.style.WARNING(f'Image not found: {img_data["path"]}'))
                    continue

                # Check if image already exists
                existing_image = Image.objects.filter(title=img_data['title']).first()
                if existing_image:
                    self.stdout.write(self.style.WARNING(f'Image already exists: {img_data["title"]}'))
                    imported_images.append(existing_image)
                    continue

                # Create new image
                with open(img_data['path'], 'rb') as image_file:
                    wagtail_image = Image(
                        title=img_data['title'],
                    )
                    wagtail_image.file.save(
                        os.path.basename(img_data['path']),
                        ImageFile(image_file),
                        save=True
                    )
                    imported_images.append(wagtail_image)
                    self.stdout.write(self.style.SUCCESS(f'✓ Imported: {img_data["title"]}'))

            if len(imported_images) < 3:
                self.stdout.write(self.style.ERROR('Not enough images imported.'))
                return

            # Update hero blocks with images
            self.stdout.write('\nUpdating hero blocks with images...')

            if not homepage.corps:
                self.stdout.write(self.style.ERROR('No content blocks found on homepage.'))
                return

            updated_blocks = []
            hero_index = 0

            for block in homepage.corps:
                if block.block_type == 'hero_block' and hero_index < len(imported_images):
                    # Update the image_fond field with the Image object
                    block_dict = dict(block.value)
                    block_dict['image_fond'] = imported_images[hero_index]
                    updated_blocks.append(('hero_block', block_dict))
                    self.stdout.write(self.style.SUCCESS(f'✓ Updated hero block {hero_index + 1}'))
                    hero_index += 1
                else:
                    # Keep other blocks as-is
                    if hasattr(block.value, '__iter__') and not isinstance(block.value, (str, bytes)):
                        updated_blocks.append((block.block_type, dict(block.value)))
                    else:
                        updated_blocks.append((block.block_type, block.value))

            # Save updated blocks
            homepage.corps = updated_blocks
            homepage.save_revision().publish()

            self.stdout.write(self.style.SUCCESS(f'\n✓ Successfully updated {hero_index} hero blocks with images!'))
            self.stdout.write(self.style.SUCCESS('\nView your homepage at: http://127.0.0.1:8000/'))
            self.stdout.write(self.style.SUCCESS('The hero blocks should now have beautiful crop field backgrounds!'))

        except Exception as exception:
            self.stdout.write(self.style.ERROR(f'Error: {str(exception)}'))
            import traceback
            traceback.print_exc()
            raise
