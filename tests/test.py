import time
from django.test import TestCase

from database_orm.context_manager import Timer
from database_orm.core.models import User, Calendar, Meeting, Attendee
from database_orm.core.views import create_user, create_bulk_user, create_calendar, create_user_using_sql, \
    create_user_using_sql_batch, create_meetings, create_attendees
from database_orm.settings import USER_COUNT, CALENDAR_NAMES, MEETING_COUNT


class TestORMSingleSave(TestCase):
    def test_create_user(self):
        total_time = create_user()
        print "ORM - Single Save {}".format(total_time)
        users = User.objects.all()
        self.assertEqual(users.count(), USER_COUNT)


class TestORMBulkSave(TestCase):
    def test_create_bulk_user(self):
        total_time = create_bulk_user()
        print "ORM - Bulk Save {}".format(total_time)
        users = User.objects.all()
        self.assertEqual(users.count(), USER_COUNT)

        # Creating Calendar
        create_calendar()
        calendar = Calendar.objects.all()
        self.assertEqual(calendar.count(), USER_COUNT*len(CALENDAR_NAMES))

        # Creating Meetings
        create_meetings()
        meetings = Meeting.objects.all()
        self.assertEqual(meetings.count(), MEETING_COUNT)

        # Creating Attendees
        create_attendees()
        attendees = Attendee.objects.all()
        self.assertEqual(attendees.count(), MEETING_COUNT)


class TestSQLSingleSave(TestCase):
    def test_create_user_using_sql(self):
        total_time = create_user_using_sql()
        print "SQL - Single Save {}".format(total_time)
        users = User.objects.all()
        self.assertEqual(users.count(), USER_COUNT)


class TestSQLBatchSave(TestCase):
    def test_create_user_using_sql_batch(self):
        total_time = create_user_using_sql_batch()
        print "SQL - Batch Save {}".format(total_time)
        users = User.objects.all()
        self.assertEqual(users.count(), USER_COUNT)
