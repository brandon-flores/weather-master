from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Customer, UserProfile, Location, Avatar


class LocationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Location
        fields = ('city', )


class AvatarSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Avatar
        fields = ('thumbnail_url', )


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    avatar = AvatarSerializer()

    class Meta:
        model = UserProfile
        fields = ('full_name', 'phone_number', 'avatar')


class CustomerSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(read_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ('user_profile', 'location')

    # def create(self, validated_data):
    #     print('asdfsadfsadf')
    #     print(validated_data)
    #     # print(validated_data['customers'])
    #     return [{}]
