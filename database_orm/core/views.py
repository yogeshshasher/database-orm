# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from random import randint

# Create your views here.
import time
from django.db import connection

from database_orm.core.models import User, Calendar
from database_orm.settings import USER_COUNT, CALENDAR_NAMES


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
