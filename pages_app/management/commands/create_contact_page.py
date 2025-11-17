from django.core.management.base import BaseCommand
from pages_app.models import ContactPage, FormField
from home.models import HomePage


class Command(BaseCommand):
    help = 'Create the Contact page with form fields'

    def handle(self, *args, **options):
        # Get the homepage (parent page)
        try:
            homepage = HomePage.objects.get(slug='home')
        except HomePage.DoesNotExist:
            self.stdout.write(self.style.ERROR('HomePage not found'))
            return

        # Check if Contact page already exists
        try:
            contact_page = ContactPage.objects.get(slug='contact')
            self.stdout.write(self.style.WARNING('Contact page already exists, updating...'))
            # Delete existing form fields to recreate them
            contact_page.form_fields.all().delete()
        except ContactPage.DoesNotExist:
            # Create new page
            contact_page = ContactPage(
                title='Contact',
                slug='contact',
            )
            homepage.add_child(instance=contact_page)
            self.stdout.write(self.style.SUCCESS('Created new Contact page'))

        # Set page content
        contact_page.introduction = '<p>Vous avez des questions, des commentaires ou souhaitez nous contacter ? Remplissez le formulaire ci-dessous et nous vous répondrons dans les plus brefs délais.</p>'

        contact_page.message_remerciement = '<p>Nous avons bien reçu votre message et nous vous répondrons dans les plus brefs délais.</p><p>Si votre demande est urgente, vous pouvez nous contacter directement par téléphone.</p>'

        # Email settings
        contact_page.to_address = 'info@victimespesticidesquebec.org'
        contact_page.from_address = 'noreply@victimespesticidesquebec.org'
        contact_page.subject = 'Nouveau message depuis le formulaire de contact'

        # Save the page first
        contact_page.save()
        contact_page.save_revision().publish()

        # Create form fields
        form_fields = [
            {
                'label': 'Nom complet',
                'field_type': 'singleline',
                'required': True,
                'sort_order': 1,
            },
            {
                'label': 'Courriel',
                'field_type': 'email',
                'required': True,
                'sort_order': 2,
            },
            {
                'label': 'Téléphone',
                'field_type': 'singleline',
                'required': False,
                'sort_order': 3,
            },
            {
                'label': 'Sujet',
                'field_type': 'singleline',
                'required': True,
                'sort_order': 4,
            },
            {
                'label': 'Message',
                'field_type': 'multiline',
                'required': True,
                'sort_order': 5,
            },
        ]

        for field_data in form_fields:
            FormField.objects.create(
                page=contact_page,
                **field_data
            )

        # Mark page as shown in menus
        contact_page.show_in_menus = True
        contact_page.save()
        contact_page.save_revision().publish()

        self.stdout.write(self.style.SUCCESS(f'✓ Contact page created/updated successfully at /{contact_page.slug}/'))
        self.stdout.write(self.style.SUCCESS(f'✓ {len(form_fields)} form fields created'))
        self.stdout.write(self.style.SUCCESS('✓ Page marked as "Show in menus"'))
        self.stdout.write(self.style.WARNING(f'\n⚠ Don\'t forget to update the email addresses in the Wagtail admin!'))
        self.stdout.write(self.style.WARNING(f'   Current to_address: {contact_page.to_address}'))
