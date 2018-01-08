# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
# Create your views here.
import time
from django.utils import timezone
from random import randint, choice

from django.db import connection

from database_orm.core.models import User, Calendar, Meeting, Attendee
from database_orm.settings import USER_COUNT, CALENDAR_NAMES, MEETING_COUNT, MEETING_PREFIX, MEETING_SUFFIX, \
    MEETING_DURATION


def create_user():
    total_time = 0
    for i in range(USER_COUNT):
        start_time = time.time()
        User.objects.create(name='User' + str(i + 1),
                            team_name='Team' + str(randint(1, 100)))
        end_time = time.time()
        total_time = total_time + (end_time - start_time)

    return total_time


def create_user_using_sql():
    total_time = 0
    cursor = connection.cursor()
    for i in range(USER_COUNT):
        name = 'User' + str(i + 1)
        team_name = 'Team' + str(randint(1, 100))
        query = "insert into core_user(name, team_name) values('{0}', '{1}')".format(name, team_name)
        start_time = time.time()
        cursor.execute(query)
        end_time = time.time()
        total_time = total_time + (end_time - start_time)
    cursor.close()
    return total_time


def create_user_using_sql_batch():
    cursor = connection.cursor()
    values_list = []
    for i in range(USER_COUNT):
        name = 'User' + str(i + 1)
        team_name = 'Team' + str(randint(1, 100))
        values_list.append("('{0}', '{1}')".format(name, team_name))

    query = "insert into core_user(name, team_name) values{}".format(','.join(values_list))
    start_time = time.time()
    cursor.execute(query)
    end_time = time.time()
    cursor.close()
    return end_time - start_time


def create_bulk_user():
    user = []
    for i in range(USER_COUNT):
        user.append(User(name='User' + str(i + 1),
                         team_name='Team'+str(randint(1, 100))))
    start_time = time.time()
    User.objects.bulk_create(user)
    end_time = time.time()
    return end_time - start_time


def create_calendar():
    calendar = []
    users = User.objects.all()
    for user in users:
        for cal in CALENDAR_NAMES:
            calendar.append(Calendar(user=user, name=cal))
    Calendar.objects.bulk_create(calendar)


def create_meetings():
    meetings = []
    calendars = list(Calendar.objects.all().values_list('id', flat=True))
    current_time = timezone.now()
    for i in range(MEETING_COUNT):
        calendar = Calendar.objects.get(id=choice(calendars))
        meetings.append(Meeting(calendar=calendar,
                                title=str(choice(MEETING_PREFIX)) + ' ' + str(choice(MEETING_SUFFIX)),
                                start_time=current_time,
                                end_time=current_time + datetime.timedelta(minutes=int(choice(MEETING_DURATION)))
                                ))
    Meeting.objects.bulk_create(meetings)


def create_attendees():
    attendees = []
    meetings = Meeting.objects.all()
    for meeting in meetings:
        user = User.objects.get(name='User'+str(randint(1, 10)))
        attendees.append(Attendee(user=user, meeting=meeting))
    Attendee.objects.bulk_create(attendees)
