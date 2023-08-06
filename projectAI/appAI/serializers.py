from rest_framework import serializers
from .models import employee, project_general,project_task

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = employee
        fields = ('id','FirstName','LastName','address','email','birthday','position')


class project_generalSerializer(serializers.ModelSerializer):
     class Meta:
        model = project_general
        fields = '__all__'

class project_taskSerializer(serializers.ModelSerializer):
     class Meta:
        model = project_task
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    