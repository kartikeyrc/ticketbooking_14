from django.core.management.base import BaseCommand
from django.utils import timezone
from booking.models import Show, Venue
from decimal import Decimal
import datetime

class Command(BaseCommand):
    help = 'Adds sample movies to the database'

    def handle(self, *args, **kwargs):
        # Create a sample venue first
        venue, _ = Venue.objects.get_or_create(
            name="CineMax Theater",
            defaults={
                'address': "123 Movie Street, Cinema City",
                'capacity': 200
            }
        )

        # Sample movies data
        movies = [
            {
                'title': "Interstellar Odyssey",
                'description': "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
                'date': timezone.now() + datetime.timedelta(days=1),
                'price': Decimal('15.99'),
                'total_seats': 100,
            },
            {
                'title': "Galactic Heist",
                'description': "A group of misfits plan the biggest heist in the galaxy, but things go hilariously wrong.",
                'date': timezone.now() + datetime.timedelta(days=2),
                'price': Decimal('14.99'),
                'total_seats': 150,
            },
            {
                'title': "Mystery of the Lost City",
                'description': "Adventurers search for a legendary city lost to time, facing ancient puzzles and traps.",
                'date': timezone.now() + datetime.timedelta(days=3),
                'price': Decimal('12.99'),
                'total_seats': 120,
            },
            {
                'title': "Robot's Last Stand",
                'description': "In a future ruled by machines, one robot dares to defy its programming for freedom.",
                'date': timezone.now() + datetime.timedelta(days=4),
                'price': Decimal('13.99'),
                'total_seats': 130,
            },
            {
                'title': "The Great Bake-Off",
                'description': "Chefs from around the world compete in a high-stakes, comedic baking competition.",
                'date': timezone.now() + datetime.timedelta(days=5),
                'price': Decimal('16.99'),
                'total_seats': 180,
            }
        ]

        for movie in movies:
            Show.objects.get_or_create(
                title=movie['title'],
                defaults={
                    'description': movie['description'],
                    'venue': venue,
                    'date': movie['date'],
                    'price': movie['price'],
                    'total_seats': movie['total_seats'],
                    'booked_seats': 0
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully added sample movies'))

 