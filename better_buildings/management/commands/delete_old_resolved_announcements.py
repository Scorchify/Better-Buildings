from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from better_buildings.models import Announcement

class Command(BaseCommand):
    help = 'Deletes resolved announcements older than 3 days'

    def handle(self, *args, **kwargs):
        three_days_ago = timezone.now() - timedelta(days=3)
        old_resolved_announcements = Announcement.objects.filter(resolved=True, resolved_date__lt=three_days_ago)
        count = old_resolved_announcements.count()
        old_resolved_announcements.delete()
        self.stdout.write(f'Successfully deleted {count} resolved announcements older than 3 days.')