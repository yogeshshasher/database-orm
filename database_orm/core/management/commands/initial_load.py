from django.core.management.base import BaseCommand

from database_orm.core import views


class Command(BaseCommand):

    def handle(self, *args, **options):
        views.create_users_using_sql_batch()
        views.create_calendars_using_sql_batch()
        views.create_meetings_using_sql_batch()
        views.create_attendees_using_sql_batch()
