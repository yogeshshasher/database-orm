# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from random import randint

# Create your views here.
from database_orm.core.models import User, Calendar
from database_orm.settings import USER_COUNT, CALENDAR_NAMES


def create_user():
    for i in range(USER_COUNT):
        User.objects.create(name='User' + str(i + 1),
                            team_name='Team' + str(randint(1, 100)))


def create_bulk_user():
    user = []
    for i in range(USER_COUNT):
        user.append(User(name='User' + str(i + 1),
                         team_name='Team'+str(randint(1, 100))))
    User.objects.bulk_create(user)


def create_calendar():
    calendar = []
    users = User.objects.all()
    for user in users:
        for cal in CALENDAR_NAMES:
            calendar.append(Calendar(user=user, name=cal))
    Calendar.objects.bulk_create(calendar)
