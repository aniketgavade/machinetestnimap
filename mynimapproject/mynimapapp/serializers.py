from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
    # This serializer will be used to include the user's name in the output
    class Meta:
        model = User
        fields = ['id', 'username']

# Client Serializer
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['name']  # This will output the client name

class ProjectSerializer(serializers.ModelSerializer):
    client = serializers.CharField(source='client.client_name')  # Fetch the client name
    users = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users', 'created_at', 'created_by']

    def get_users(self, obj):
        return [{'id': user.id, 'name': user.username} for user in obj.users.all()]
    
    def create(self, validated_data):
        # Extract user data and associate it with the project
        users_data = validated_data.pop('users')
        project = Project.objects.create(**validated_data)
        
        # If there are users to be assigned, set them
        project.users.set(users_data)
        
        return project
# Serializer for Project
class ProjectSerializer(serializers.ModelSerializer):
    
    # Retrieve the client name from the related client instance
    client_name = serializers.CharField(source='client.client_name', read_only=True)
    
    # Retrieve the username of the user who created the project
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    
    # Format the created_at field to match the requested format
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client_name', 'created_at', 'created_by']    

# Serializer for Client
class ClientSerializer(serializers.ModelSerializer):
    # Include the 'created_by' as the username (not just the user id)
    created_by = serializers.CharField(source='created_by.username')

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by', 'updated_at']


# Serializer for Client with Projects
class ClientWithProjectsSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)  # Include projects for client

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by', 'projects']


# Serializer for Project
from rest_framework import serializers
from .models import Project

class AProjectSerializer(serializers.ModelSerializer):
    # Retrieve the client name from the related client instance
    client_name = serializers.CharField(source='client.client_name', read_only=True)
    
    # Retrieve the username of the user who created the project
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    
    # Format the created_at field to match the requested format
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%f%z", read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client_name', 'created_at', 'created_by']



# Serializer for Client with Projects
class ClientWithProjectsSerializer(serializers.ModelSerializer):
    # Include related projects
    projects = ProjectSerializer(many=True, read_only=True)

    # Formatting date fields as requested
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField( read_only=True)
    
    # Include 'created_by' as username
    created_by = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'projects', 'created_at', 'created_by', 'updated_at']

