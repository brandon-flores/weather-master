# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Avatar(models.Model):
    large_url = models.URLField(max_length=255, null=True, blank=True)
    medium_url = models.URLField(max_length=255, null=True, blank=True)
    thumbnail_url = models.URLField(max_length=255, null=True, blank=True)


class Street(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return '{} {}'.format(self.number, self.name)


class Location(models.Model):
    street = models.ForeignKey(
        Street, on_delete=models.SET_NULL, related_name='locations',
        null=True, blank=True)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return '{}, {}, {}'.format(self.street, self.city, self.country)


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
    avatar = models.ForeignKey(
        Avatar, on_delete=models.SET_NULL, related_name='user_profiles',
        null=True, blank=True)

    @property
    def full_name(self):
        return '{} {} {}'.format(self.title, self.first_name, self.last_name)

    def __str__(self):
        return self.full_name


class Customer(models.Model):
    user_profile = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name='customer')
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, related_name='customers',
        null=True, blank=True)

    @property
    def full_name(self):
        return self.user_profile.full_name
