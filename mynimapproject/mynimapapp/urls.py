from django.urls import path
from . import views

urlpatterns = [
    # Client endpoints
    path('clients/', views.client_list_view, name='client-list'),  # List all clients
    path('clients/new/', views.create_client_view, name='create-client'),  # Create a new client
    path('clients/<int:id>/', views.client_detail_with_projects, name='client-detail'),  # Get client details with projects
    path('clients/<int:id>/update/', views.update_client_view, name='update-client'),  # Update client details
    path('clients/<int:id>/delete/', views.delete_client_view, name='delete-client'),  # Delete a client
    
    # Project endpoints

    path('projects/', views.create_project_view, name='create-project'),  # Create a new project
    path('projects/list', views.project_list_view, name='project-list'),
    path('projects/assigned_to_user/', views.projects_assigned_to_user, name='projects-assigned-to-user'),  # Get projects assigned to the logged-in user
]
