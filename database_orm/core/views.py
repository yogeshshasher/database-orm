# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
# Create your views here.
import time

from django.db.models import Q
from django.utils import timezone
from random import randint, choice

from django.db import connection

from database_orm.context_manager import NumOfQueries
from database_orm.core.models import User, Calendar, Meeting, Attendee
from database_orm.settings import USER_COUNT, CALENDAR_NAMES, MEETING_COUNT, MEETING_PREFIX, MEETING_SUFFIX, \
    MEETING_DURATION


# Creating entries through ORM single save

def create_users():
    total_time = 0
    for i in range(USER_COUNT):
        start_time = time.time()
        User.objects.create(name='User' + str(i + 1),
                            team_name='Team' + str(randint(1, 100)))
        end_time = time.time()
        total_time = total_time + (end_time - start_time)

    return total_time


def create_calendars():
    total_time = 0
    users = User.objects.all()
    for user in users:
        for cal in CALENDAR_NAMES:
            start_time = time.time()
            Calendar.objects.create(user=user, name=cal)
            end_time = time.time()
            total_time = total_time + (end_time - start_time)
    return total_time


def create_meetings():
    total_time = 0
    calendars = list(Calendar.objects.all().values_list('id', flat=True))
    current_time = timezone.now()
    for i in range(MEETING_COUNT):
        calendar = Calendar.objects.get(id=choice(calendars))
        start_time = time.time()
        Meeting.objects.create(calendar=calendar,
                               title=str(choice(MEETING_PREFIX)) + ' ' + str(choice(MEETING_SUFFIX)),
                               start_time=current_time,
                               end_time=current_time + datetime.timedelta(minutes=int(choice(MEETING_DURATION))))
        end_time = time.time()
        total_time = total_time + (end_time - start_time)
    return total_time


def create_attendees():
    total_time = 0
    meetings = Meeting.objects.all()
    for meeting in meetings:
        user = User.objects.get(name='User' + str(randint(1, 10)))
        start_time = time.time()
        Attendee.objects.create(user=user, meeting=meeting)
        end_time = time.time()
        total_time = total_time + (end_time - start_time)
    return total_time


# Creating entries through ORM bulk create

def create_bulk_users():
    user = []
    for i in range(USER_COUNT):
        user.append(User(name='User' + str(i + 1),
                         team_name='Team' + str(randint(1, 100))))
    start_time = time.time()
    User.objects.bulk_create(user)
    end_time = time.time()
    return end_time - start_time


def create_bulk_calendars():
    calendar = []
    users = User.objects.all()
    for user in users:
        for cal in CALENDAR_NAMES:
            calendar.append(Calendar(user=user, name=cal))
    start_time = time.time()
    Calendar.objects.bulk_create(calendar)
    end_time = time.time()
    return end_time - start_time


def create_bulk_meetings():
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
    start_time = time.time()
    Meeting.objects.bulk_create(meetings)
    end_time = time.time()
    return end_time - start_time


def create_bulk_attendees():
    attendees = []
    meetings = Meeting.objects.all()
    for meeting in meetings:
        user = User.objects.get(name='User' + str(randint(1, 10)))
        attendees.append(Attendee(user=user, meeting=meeting))
    start_time = time.time()
    Attendee.objects.bulk_create(attendees)
    end_time = time.time()
    return end_time - start_time


# Creating entries through SQL single INSERT

def create_users_using_sql():
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


def create_calendars_using_sql():
    total_time = 0
    cursor = connection.cursor()
    users = list(User.objects.all().values_list('id', flat=True))
    for user in users:
        for cal in CALENDAR_NAMES:
            query = "INSERT into core_calendar(name, user_id) VALUES('{0}', {1})".format(cal, user)
            start_time = time.time()
            cursor.execute(query)
            end_time = time.time()
            total_time = total_time + (end_time - start_time)
    cursor.close()
    return total_time


def create_meetings_using_sql():
    total_time = 0
    cursor = connection.cursor()
    calendars = list(Calendar.objects.all().values_list('id', flat=True))
    current_time = timezone.now().replace(tzinfo=None)
    for i in range(MEETING_COUNT):
        title = str(choice(MEETING_PREFIX)) + ' ' + str(choice(MEETING_SUFFIX))
        start_time = current_time
        end_time = current_time + datetime.timedelta(minutes=int(choice(MEETING_DURATION)))
        calendar_id = choice(calendars)
        query = "INSERT into core_meeting(title, start_time, end_time, calendar_id) VALUES('{0}', '{1}', '{2}', {3})".\
            format(title, start_time, end_time, calendar_id)
        start_time = time.time()
        cursor.execute(query)
        end_time = time.time()
        total_time = total_time + (end_time - start_time)
    cursor.close()
    return total_time


def create_attendees_using_sql():
    total_time = 0
    cursor = connection.cursor()
    meetings = list(Meeting.objects.all().values_list('id', flat=True))
    for meeting in meetings:
        user = User.objects.get(name='User' + str(randint(1, 10))).id
        query = "INSERT INTO core_attendee(user_id, meeting_id) VALUES({0}, {1})".format(user, meeting)
        start_time = time.time()
        cursor.execute(query)
        end_time = time.time()
        total_time = total_time + (end_time - start_time)
    cursor.close()
    return total_time


# Creating entries through SQL multiple INSERT

def create_users_using_sql_batch():
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


def create_calendars_using_sql_batch():
    cursor = connection.cursor()
    values_list = []
    users = list(User.objects.all().values_list('id', flat=True))
    for user in users:
        for cal in CALENDAR_NAMES:
            values_list.append("('{0}', {1})".format(cal, user))

    query = "insert into core_calendar(name, user_id) values{}".format(','.join(values_list))
    start_time = time.time()
    cursor.execute(query)
    end_time = time.time()
    cursor.close()
    return end_time - start_time


def create_meetings_using_sql_batch():
    cursor = connection.cursor()
    values_list = []
    calendars = list(Calendar.objects.all().values_list('id', flat=True))
    current_time = timezone.now().replace(tzinfo=None)
    for i in range(MEETING_COUNT):
        title = str(choice(MEETING_PREFIX)) + ' ' + str(choice(MEETING_SUFFIX))
        start_time = current_time
        end_time = current_time + datetime.timedelta(minutes=int(choice(MEETING_DURATION)))
        calendar_id = choice(calendars)
        values_list.append("('{0}', '{1}', '{2}', {3})".format(title, start_time, end_time, calendar_id))

    query = "insert into core_meeting(title, start_time, end_time, calendar_id) values{}".format(','.join(values_list))
    start_time = time.time()
    cursor.execute(query)
    end_time = time.time()
    cursor.close()
    return end_time - start_time


def create_attendees_using_sql_batch():
    cursor = connection.cursor()
    values_list = []
    meetings = list(Meeting.objects.all().values_list('id', flat=True))
    for meeting in meetings:
        user = User.objects.get(name='User' + str(randint(1, 10))).id
        values_list.append("({0}, {1})".format(user, meeting))

    query = "insert into core_attendee(user_id, meeting_id) values{}".format(','.join(values_list))
    start_time = time.time()
    cursor.execute(query)
    end_time = time.time()
    cursor.close()
    return end_time - start_time


# Delete all entries from respective models

def delete_all_users():
    User.objects.all().delete()


def delete_all_calendars():
    Calendar.objects.all().delete()


def delete_all_meetings():
    Meeting.objects.all().delete()


def delete_all_attendees():
    Attendee.objects.all().delete()


# Select all attendees for Daily Scrum Meeting through filter
def select_attendee_with_daily_scrum():
    with NumOfQueries('select_attendee'):
        attendees = Attendee.objects.all()
        for attendee in attendees:
            print attendee.user


# Select all attendees for Daily Scrum Meeting through select_related
def select_attendee_with_daily_scrum_select_related():
    with NumOfQueries('select_attendee_select_related'):
        attendees = Attendee.objects.select_related('user').all()
        for attendee in attendees:
            print attendee.user


# Select all attendees for Daily Scrum Meeting through prefetch_related
def select_attendee_with_daily_scrum_prefect_related():
    attendees = Attendee.objects.all().values_list('user', flat=True)
    with NumOfQueries('select_attendee_prefect_related'):
        users = User.objects.prefetch_related('user_attendee').filter(id__in=attendees)
        for user in users:
            print user
