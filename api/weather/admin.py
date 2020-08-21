# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from api.weather.models import (
    Avatar, Location, UserProfile, Customer, Street)


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_url', )


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    model = Street


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    model = Location


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'location')
