from django.urls import path
from .views import (
    UserTaskListView,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    PermittedUsersListView,
    PermittedUserDeleteView,
    PermittedUserAddView,
    PermittedUserUpdateView,
    CommentUpdateView,
    CommentDeleteView,
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

    path('<int:pk>/comment/<int:comment_id>/update/',
         CommentUpdateView.as_view(), name='comment-update',),
    path('<int:pk>/comment/<int:comment_id>/delete/',
         CommentDeleteView.as_view(), name='comment-delete'),
]
