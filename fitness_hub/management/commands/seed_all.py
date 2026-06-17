"""Master seed command — runs all seeders in dependency order.

Keeps existing per-app seed commands intact. This file is the single
entry point to populate every data table from scratch.

Usage:
    python manage.py seed_all
"""
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Seed all data: exercises, inspiration, store, achievements.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('=== Seeding all data ==='))
        self.stdout.write('')

        order = [
            ('exercises', 'seed_exercises'),
            ('inspiration', 'seed_inspiration'),
            ('store', 'seed_store'),
            ('achievements', 'seed_achievements'),
        ]

        for app, cmd in order:
            self.stdout.write(self.style.WARNING(f'-- {cmd} --'))
            call_command(cmd)
            self.stdout.write('')

        self.stdout.write(self.style.SUCCESS('=== All seeds complete ==='))
