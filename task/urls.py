from django.urls import path
from .views import (
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    UserTaskListView,
    PermittedUsersListView,
    PermittedUsersCreateView,
    PermittedUserDeleteView,
)


urlpatterns = [
    path('explore/', TaskListView.as_view(), name='tasks-explore'),
    path('user/<str:username>', UserTaskListView.as_view(), name='user-tasks'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/new/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('tasks/<int:pk>/permitted-users/', PermittedUsersListView.as_view(), name='permitted-users'),
    path('tasks/<int:pk>/permitted-user-add/', PermittedUsersCreateView.as_view(), name='permitted-user-add'),
    path('tasks/<int:pk>/permitted-users/delete/<int:permission_pk>', PermittedUserDeleteView.as_view(), name='permitted-user-delete'),
]
