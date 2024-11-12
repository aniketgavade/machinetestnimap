# views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer, UserSerializer
from django.contrib.auth.models import User

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def retrieve(self, request, pk=None):
        client = self.get_object()
        serializer = ClientSerializer(client)
        client_data = serializer.data
        
        projects = client.projects.all()
        project_serializer = ProjectSerializer(projects, many=True)
        client_data['projects'] = project_serializer.data
        
        return Response(client_data)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        print("Request data received:", request.data)  # View all incoming data
        client_id = request.data.get('client_id')
        print("client_id extracted:", client_id)  # Confirm if client_id is None here

        users = request.data.get('users', [])

        if not client_id:
            return Response({'error': 'client_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)

        # Fetch the users specified in the request
        user_objs = User.objects.filter(id__in=users)

        # Pass data to serializer and check for validity
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save project with the client and created_by user
            project = serializer.save(client=client, created_by=request.user)
            project.users.set(user_objs)  # Assign users to project
            project.save()

            # Return serialized project data with 201 status
            return Response(ProjectSerializer(project).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def assigned_to_user(self, request):
        user_projects = Project.objects.filter(users=request.user)
        serializer = ProjectSerializer(user_projects, many=True)
        return Response(serializer.data)
