from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Placeholder command retained for compatibility; OpenAI integration has been removed.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('OpenAI integration is disabled. The chatbot uses built-in responses instead.'))
