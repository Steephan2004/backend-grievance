# import serializers from the REST framework
from rest_framework import serializers

# import the todo data model
from .models import *

# create a serializer class
class LoginSerializer(serializers.ModelSerializer):
    # create a meta class
    class Meta:
        model = Login
        fields = "__all__"

# create a serializer class
class GuestLoginSerializer(serializers.ModelSerializer):
    # create a meta class
    class Meta:
        model = GuestLogin
        fields = ('id', 'Name', 'MobileNumber')

class AdminLoginSerializer(serializers.ModelSerializer):
    # create a meta class
    class Meta:
        model = AdminLogin
        fields = "__all__"
  
class QueryFormSerializer(serializers.ModelSerializer):

    class Meta:
        model = QueryForm
        fields = '__all__'
