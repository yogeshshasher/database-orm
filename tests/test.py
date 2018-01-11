from django.test import TestCase

from database_orm.core.models import User, Calendar, Meeting, Attendee
from database_orm.core import views
from database_orm.settings import USER_COUNT, CALENDAR_NAMES, MEETING_COUNT


class TestORMSingleSave(TestCase):
    def test_create_user(self):
        t1 = views.create_users()
        t2 = views.create_calendars()
        t3 = views.create_meetings()
        t4 = views.create_attendees()
        print "ORM - Single Save {}".format(t1 + t2 + t3 + t4)

        attendees = Attendee.objects.all()
        self.assertEqual(attendees.count(), MEETING_COUNT)


class TestORMBulkSave(TestCase):
    def test_create_bulk_user(self):
        t1 = views.create_bulk_users()
        t2 = views.create_bulk_calendars()
        t3 = views.create_bulk_meetings()
        t4 = views.create_bulk_attendees()
        print "ORM - Bulk Save {}".format(t1 + t2 + t3 + t4)

        attendees = Attendee.objects.all()
        self.assertEqual(attendees.count(), MEETING_COUNT)


class TestSQLSingleSave(TestCase):
    def test_create_user_using_sql(self):
        t1 = views.create_users_using_sql()
        t2 = views.create_calendars_using_sql()
        t3 = views.create_meetings_using_sql()
        t4 = views.create_attendees_using_sql()
        print "SQL - Single Save {}".format(t1 + t2 + t3 + t4)

        attendees = Attendee.objects.all()
        self.assertEqual(attendees.count(), MEETING_COUNT)


class TestSQLBatchSave(TestCase):
    def test_create_user_using_sql_batch(self):
        t1 = views.create_users_using_sql_batch()
        t2 = views.create_calendars_using_sql_batch()
        t3 = views.create_meetings_using_sql_batch()
        t4 = views.create_attendees_using_sql_batch()
        print "SQL - Batch Save {}".format(t1 + t2 + t3 + t4)

        attendees = Attendee.objects.all()
        self.assertEqual(attendees.count(), MEETING_COUNT)
