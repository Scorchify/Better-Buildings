from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from better_buildings.models import Report

class Command(BaseCommand):
    help = 'Deletes resolved reports older than 3 days'

    def handle(self, *args, **kwargs):
        three_days_ago = timezone.now() - timedelta(days=3)
        old_resolved_reports = Report.objects.filter(resolved=True, resolved_date__lt=three_days_ago)
        count = old_resolved_reports.count()
        old_resolved_reports.delete()
        self.stdout.write(f'Successfully deleted {count} resolved reports older than 3 days.')