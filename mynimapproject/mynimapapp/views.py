from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Client, Project
from .serializers import ClientSerializer, ClientWithProjectsSerializer, ProjectSerializer
from rest_framework import status

# List all clients
@api_view(['GET'])
def client_list_view(request):
    clients = Client.objects.all()
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)

# Create a new client
@api_view(['POST'])
def create_client_view(request):
    if request.user.is_authenticated:
        client_name = request.data.get('client_name')
        
        if not client_name:
            return Response({'error': 'Client name is required'}, status=400)

        client = Client.objects.create(client_name=client_name, created_by=request.user)

        return Response(ClientSerializer(client).data)
    return Response({'error': 'Authentication required'}, status=401)

# Get client details with projects
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Client
from .serializers import ClientWithProjectsSerializer

@api_view(['GET'])
def client_detail_with_projects(request, id):
    try:
        # Fetch the client by ID
        client = Client.objects.get(id=id)
    except Client.DoesNotExist:
        return Response({'error': 'Client not found'}, status=404)

    # Serialize the client data along with associated projects
    serializer = ClientWithProjectsSerializer(client)
    return Response(serializer.data)


# Update client details
@api_view(['PUT', 'PATCH'])
def update_client_view(request, id):
    try:
        client = Client.objects.get(id=id)
    except Client.DoesNotExist:
        return Response({'error': 'Client not found'}, status=404)

    serializer = ClientSerializer(client, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


# Delete a client
@api_view(['DELETE'])
def delete_client_view(request, id):
    try:
        client = Client.objects.get(id=id)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Client.DoesNotExist:
        return Response({'error': ' 204 No Content'}, status=status.HTTP_404_NOT_FOUND)
# Create a new project and assign it to a client with users

@api_view(['POST'])
def create_project_view(request):
    project_name = request.data.get('project_name')
    client_id = request.data.get('client_id')
    user_ids = request.data.get('users', [])

    # Ensure that all required fields are provided
    if not (project_name and client_id and user_ids):
        return Response({'error': 'Project name, client ID, and users are required'}, status=400)

    # Check if the client exists
    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return Response({'error': 'Client not found'}, status=404)

    # Get users specified in the request
    users = User.objects.filter(id__in=user_ids)

    # Create the project
    project = Project.objects.create(
        project_name=project_name,
        client=client,
        created_by=request.user
    )

    # Assign users to the project
    project.users.set(users)
    project.save()

    # Prepare the response data
    response_data = ProjectSerializer(project).data

    # Add formatted output for the client and users
    response_data['client'] = client.client_name  # Add the client name instead of client ID
    response_data['users'] = [{"id": user.id, "name": user.username} for user in users]  # Add user names

    # Add created_at and created_by fields if needed
    response_data['created_at'] = project.created_at.isoformat()  # Format timestamp
    response_data['created_by'] = project.created_by.username

    return Response(response_data, status=status.HTTP_201_CREATED)
# mynimapapp/views.py


# List projects assigned to the logged-in user

@api_view(['GET'])
def projects_assigned_to_user(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

    # Fetch the projects assigned to the user
    user_projects = Project.objects.filter(users=request.user)

    # If no projects found, return a message or 204 (No Content)
    if not user_projects.exists():
        return Response({"message": "No projects assigned to this user"}, status=status.HTTP_204_NO_CONTENT)

    # Serialize the user-specific projects
    serializer = ProjectSerializer(user_projects, many=True)

    # Return serialized data
    return Response(serializer.data)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Project
from .serializers import AProjectSerializer

@api_view(['GET'])
def project_list_view(request):
    # Fetch all projects
    projects = Project.objects.all()
    
    # Serialize the projects data
    serializer = AProjectSerializer(projects, many=True)
    
    # Return the serialized data
    return Response(serializer.data)
