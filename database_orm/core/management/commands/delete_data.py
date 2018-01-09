from django.core.management.base import BaseCommand

from database_orm.core import views


class Command(BaseCommand):

    def handle(self, *args, **options):
        views.delete_all_attendees()
        views.delete_all_meetings()
        views.delete_all_calendars()
        views.delete_all_users()
