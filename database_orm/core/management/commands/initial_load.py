from django.core.management.base import BaseCommand

from database_orm.core import views


class Command(BaseCommand):

    def handle(self, *args, **options):
        views.create_bulk_user()
        views.create_calendar()
        views.create_meetings()
        views.create_attendees()
