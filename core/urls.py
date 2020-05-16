from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    MainPageRedirectView,
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
    path('', MainPageRedirectView.as_view(), name='home-redirect'),
    path('explore/', TaskListView.as_view(), name='tasks-explore'),
    path('user/<str:username>', UserTaskListView.as_view(), name='user-tasks'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/new/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/update/',
         TaskUpdateView.as_view(),
         name='task-update'),
    path('tasks/<int:pk>/delete/',
         TaskDeleteView.as_view(),
         name='task-delete'),
    path('tasks/<int:pk>/permitted-users/',
         PermittedUsersListView.as_view(),
         name='permitted-users'),
    path('tasks/<int:pk>/permitted-user-add/',
         PermittedUserAddView.as_view(),
         name='permitted-user-add'),
    path('tasks/<int:pk>/permitted-users/update/<int:user_id>',
         PermittedUserUpdateView.as_view(),
         name='permitted-user-update'),
    path('tasks/<int:pk>/permitted-users/delete/<int:user_id>',
         PermittedUserDeleteView.as_view(),
         name='permitted-user-delete'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
