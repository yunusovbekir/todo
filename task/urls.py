from django.urls import path
from .views import (
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    UserTaskListView,
    PermittedUsersListView,
    PermittedUserDeleteView,
    PermittedUserAddView,
    PermittedUserUpdateView,
)


urlpatterns = [
    path('', TaskListView.as_view(), name='tasks-explore'),
    path('user/<str:username>/', UserTaskListView.as_view(),
         name='user-tasks'),

    path('new/', TaskCreateView.as_view(), name='task-create'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),

    path('<int:pk>/permitted-users/', PermittedUsersListView.as_view(),
         name='permitted-users'),
    path('<int:pk>/permitted-user-add/', PermittedUserAddView.as_view(),
         name='permitted-user-add'),
    path('<int:pk>/permitted-users/update/<str:username>/',
         PermittedUserUpdateView.as_view(),
         name='permitted-user-update'),
    path('<int:pk>/permitted-users/delete/<str:username>/',
         PermittedUserDeleteView.as_view(),
         name='permitted-user-delete'),
]
