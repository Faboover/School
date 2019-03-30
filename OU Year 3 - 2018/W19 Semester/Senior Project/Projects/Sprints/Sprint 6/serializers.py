from api.models import Parent, Device, Event, Bus, Driver, Student, School
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'first_name', 'last_name', 'email', 'is_active')
        read_only_fields = ('last_login','date_joined')

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ('user','phone_number','address','city','state','zipcode')

class ParentUserSerializer(serializers.ModelSerializer):
    parent = ParentSerializer()
    def to_representation(self, obj):
        representation = super().to_representation(obj)
        parent_representation = representation.pop('parent')
        if(parent_representation is not None):
            for key in parent_representation:
                representation[key] = parent_representation[key]
        return representation
    
    def to_internal_value(self, data):
        parent_internal = {}
        for key in ParentSerializer.Meta.fields:
            if key in data:
                parent_internal[key] = data.pop(key)
        internal = super().to_internal_value(data)
        internal['parent'] = parent_internal
        return internal
    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data["username"],
            first_name = validated_data["first_name"],
            last_name = validated_data["last_name"],
            email = validated_data["email"],
            is_active = validated_data["is_active"])
        parent_data = validated_data.pop('parent')
        parent = Parent.objects.create(
            user = user,
            phone_number = parent_data["phone_number"],
            address = parent_data["address"],
            city = parent_data["city"],
            state = parent_data["state"],
            zipcode = parent_data["zipcode"])
        return user
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_active','parent')
        read_only_fields = ('last_login','date_joined')
        
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('user','registered_by','bus')

class DeviceUserSerializer(serializers.ModelSerializer):
    device = DeviceSerializer()
    
    def to_representation(self, obj):
        representation = super().to_representation(obj)
        device_representation = representation.pop('device')
        if(device_representation is not None):
            for key in device_representation:
                representation[key] = device_representation[key]
        return representation
    
    def to_internal_value(self, data):
        device_internal = {}
        for key in ParentSerializer.Meta.fields:
            if key in data:
                device_internal[key] = data.pop(key)
        internal = super().to_internal_value(data)
        internal['device'] = device_internal
        return internal

    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data["username"],
            is_active = validated_data["is_active"])
        device_data = validated_data.pop('device')
        device = Device.objects.create(
            user = user)
        return user
        
    class Meta:
        model = User
        fields = ('username','is_active','device')
        read_only_fields = ('last_login','date_joined')
		
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id','first_name','last_name','age','grade','school','bus','picture','parent_one','parent_two', 'track')

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('enter','timestamp','picture','device','student')

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ('id','name',)
        
class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ('id','bus','first_name','last_name')

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('id','name','address','city','state','zipcode')
