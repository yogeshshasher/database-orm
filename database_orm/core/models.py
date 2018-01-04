# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models


class User(models.Model):
    name = models.CharField(max_length=2047)
    team_name = models.CharField(max_length=2047)


class Calendar(models.Model):
    user = models.ForeignKey(User, related_name="calendar_owner", unique=True)
    name = models.CharField(max_length=2047)


class Meeting(models.Model):
    calendar = models.ForeignKey(Calendar, related_name="calendar")
    meeting_id = models.CharField(max_length=1040)
    hashed_id = models.CharField(max_length=255)
    title = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)


class Attendee(models.Model):
   meeting = models.ForeignKey(Meeting, related_name="attendee")
   user = models.ForeignKey(User, null=True, blank=True, related_name="user_attendee")