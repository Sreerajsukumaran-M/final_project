from django.core.management.base import BaseCommand
from django.utils import timezone
from offer.models import Offer

class Command(BaseCommand):
    help = 'Deactivate expired offers'

    def handle(self, *args, **options):
        now = timezone.now()
        expired_offers = Offer.objects.filter(end_date__lt=now, is_active=True)
        
        count = expired_offers.count()
        expired_offers.update(is_active=False)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully deactivated {count} expired offers'))