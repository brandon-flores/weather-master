# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import ast
import json
from django.db import transaction
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from .models import Customer, UserProfile, Street, Avatar, Location
from .serializers import CustomerSerializer
from django.views.generic import View
from django.http import JsonResponse


class CustomerListView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    # def create(self, request, *args, **kwargs):
    #     print('im herrrrrrrrrrrreeeeeeeeeeeeeeeeeeeeeeee')
    #     print(request.data)
    #     print(args)
    #     print(kwargs)
    #     # your custom implementation goes here

    #     return Response()


class CSVLoadView(View):

    def post(self, request, *args, **kwargs):
        customers = request.POST.get('customers')
        if (not request.is_ajax or not customers):
            return JsonResponse(None, status=400)
        customers = ast.literal_eval(customers)
        # 'gender', 'name.title', 'name.first', 'name.last',
        # 'location.street.number', 'location.street.name',
        # 'location.city', 'location.country', 'phone', 'picture.large',
        # 'picture.medium', 'picture.thumbnail'
        with transaction.atomic():
            for customer in customers:
                gender = (
                    UserProfile.FEMALE
                    if 'female' in customer['gender']
                    else UserProfile.MALE)

                avatar, created = Avatar.objects.get_or_create(
                    large_url=customer['picture.large'],
                    medium_url=customer['picture.medium'],
                    thumbnail_url=customer['picture.thumbnail'])

                user_profile, created = UserProfile.objects.get_or_create(
                    gender=gender, title=customer['name.title'],
                    first_name=customer['name.first'],
                    last_name=customer['name.last'],
                    phone_number=customer['phone'],
                    avatar=avatar)

                street, created = Street.objects.get_or_create(
                    number=customer['location.street.number'],
                    name=customer['location.street.name'])

                location, created = Location.objects.get_or_create(
                    city=customer['location.city'],
                    country=customer['location.country'], street=street)

                Customer.objects.get_or_create(
                    user_profile=user_profile, location=location)
            # print(customer)
        # instance_id = str(request.GET.get('pk', None))
        # if (not request.is_ajax or
        #         instance_id is None or not instance_id.isdigit()):
        #     return JSONResponse(None, status=400)
        # instance = BIRForm2307.objects.filter(
        #     pk=instance_id, status=BIRForm2307.PENDING).first()
        # if instance is None:
        #     return JSONResponse(dict(data="Instance not found"), status=400)
        # form = BIRForm2307UpdateForm(
        #     data=request.POST, instance=instance)
        # if form.is_valid():
        #     form.save()
        #     return JSONResponse(None, status=200)
        # return JSONResponse(dict(data=form.errors), status=400)
