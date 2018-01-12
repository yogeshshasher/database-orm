from django.core.management.base import BaseCommand

from database_orm.core import views


class Command(BaseCommand):

    def handle(self, *args, **options):
        views.select_attendee_with_daily_scrum_prefetch_related()
