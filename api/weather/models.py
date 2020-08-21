# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Avatar(models.Model):
    large_url = models.URLField(max_length=255, null=True)
    medium_url = models.URLField(max_length=255, null=True)
    thumbnail_url = models.URLField(max_length=255, null=True)


class Location(models.Model):
    street_number = models.CharField(max_length=255, null=True)
    street_name = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)

    def __str__(self):
        return "{} {}, {}, {}".format(
            self.street_number, self.street_name, self.city, self.country)


class UserProfile(models.Model):
    FEMALE = 1
    MALE = 2
    SEX_CHOICES = (
        (FEMALE, 'Female'),
        (MALE, 'Male'),)

    gender = models.IntegerField(choices=SEX_CHOICES, null=True, blank=True)
    title = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    avatar = models.OneToOneField(
        Avatar, on_delete=models.SET_NULL, related_name='user_profile',
        null=True, blank=True)

    def __str__(self):
        return "{} {} {}".format(self.title, self.first_name, self.last_name)


class Customer(models.Model):
    user_profile = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name='customer')
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, related_name='customers',
        null=True, blank=True)
