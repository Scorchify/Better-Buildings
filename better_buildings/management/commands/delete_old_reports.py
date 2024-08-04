from django.core.management.base import BaseCommand
from better_buildings.models import Report
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Delete reports older than one week'

    def handle(self, *args, **kwargs):
        week_ago = timezone.now() - timedelta(weeks=1)
        Report.objects.filter(resolved=True, resolved_date__lt=week_ago).delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted old reports'))