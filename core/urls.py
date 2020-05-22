from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    IndexView,
    ContactView,
    ContactMessageView,
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
    EmailTemplateTestView,
)

TASK_URL_PATTERNS = [
    path('user/<str:username>/',
         UserTaskListView.as_view(), name='user-tasks'),
    path('tasks/new/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(),
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
    path('tasks/<int:pk>/permitted-users/update/<str:username>/',
         PermittedUserUpdateView.as_view(),
         name='permitted-user-update'),
    path('tasks/<int:pk>/permitted-users/delete/<str:username>/',
         PermittedUserDeleteView.as_view(),
         name='permitted-user-delete'),
]

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('email/', EmailTemplateTestView.as_view(), name='email'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact-form/', ContactMessageView.as_view(), name='contact-form'),
    path('explore/', TaskListView.as_view(), name='tasks-explore'),
] + TASK_URL_PATTERNS

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
