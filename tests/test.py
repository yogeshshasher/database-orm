from django.test import TestCase

from database_orm.core.models import User, Calendar
from database_orm.core.views import create_user, create_bulk_user, create_calendar
from database_orm.settings import USER_COUNT, CALENDAR_NAMES


class TestDatabase(TestCase):
    def setUp(self):
        pass

    def test_create_user(self):
        create_user()
        users = User.objects.all()
        self.assertEqual(users.count(), USER_COUNT)

    def test_create_bulk_user(self):
        create_bulk_user()
        users = User.objects.all()
        self.assertEqual(users.count(), USER_COUNT)

        create_calendar()
        calendar = Calendar.objects.all()
        self.assertEqual(calendar.count(), USER_COUNT*len(CALENDAR_NAMES))
