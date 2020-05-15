from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib.auth import get_user_model
from django.views import generic
from django.utils.translation import ugettext as _
from .forms import (
    CommentForm,
    TaskForm,
    PermittedUsersForm,
    PermittedUserAddForm,
)
from .models import Task, Comment, Permitted_Users, Permitted_User

User = get_user_model()


class MainPageRedirectView(LoginRequiredMixin, generic.RedirectView):
    permanent = False
    pattern_name = 'tasks-explore'


class TaskListView(LoginRequiredMixin, generic.ListView):
    """
    return request user's tasks and the ones request user is allowed to see
    """
    model = Task
    template_name = 'task/explore.html'
    context_object_name = 'tasks'
    ordering = ['-date_created']

    def get_queryset(self):

        # request user's tasks
        task_list_1 = Task.objects.filter(author=self.request.user)

        # the ones request user is allowed to see
        user_list_1 = Task.objects.filter(
            permitted_user__read_only_users=self.request.user
        )
        user_list_2 = Task.objects.filter(
            permitted_user__comment_allowed_users=self.request.user
        )
        return task_list_1 | user_list_1 | user_list_2


class UserTaskListView(LoginRequiredMixin, generic.ListView):
    """
    If request user is the owner of the profile, return all tasks
    else return those tasks that the request user is allowed
    """

    model = Task
    template_name = 'task/user_tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        tasks = Task.objects.filter(
            author__username=self.kwargs.get('username')
        )
        if self.request.user.username == self.kwargs.get('username'):
            return tasks
        else:
            tasks_list = []
            for task in tasks:
                obj = task.permitted_user_set.first()
                allowed_users_queryset = (
                        obj.read_only_users.all() |
                        obj.comment_allowed_users.all()
                )
                allowed_users = [user for user in allowed_users_queryset]
                if self.request.user in allowed_users:
                    tasks_list.append(task)
            return tasks_list


class TaskDisplayDetailView(
    LoginRequiredMixin, UserPassesTestMixin, generic.DetailView,
):
    """
    Allow only owner of the task and allowed users
    """
    model = Task
    template_name = 'task/task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        task = self.get_object()
        obj = task.permitted_user_set.first()
        if (
                self.request.user in obj.comment_allowed_users.all() or
                self.request.user == task.author
        ):
            context['is_allowed'] = True

        context['comments'] = Comment.objects.all()  # show comments
        context['comment_form'] = CommentForm()  # show comment form
        return context

    def test_func(self):
        obj = self.get_object()
        permitted_users_object = obj.permitted_user_set.first()

        permitted_users = (
                permitted_users_object.read_only_users.all() |
                permitted_users_object.comment_allowed_users.all()
        )

        allowed_users = [user for user in permitted_users]

        return (
                self.request.user == obj.author or
                self.request.user in allowed_users
        )


class CommentView(
    LoginRequiredMixin, UserPassesTestMixin, generic.CreateView
):
    """
    Allow only the task owner and those who are allowed to comment on.
    """
    model = Comment
    form_class = CommentForm
    template_name = 'task/task_detail.html'

    def form_valid(self, form):
        form.instance.username = self.request.user
        form.instance.task_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('task-detail', args=[self.kwargs['pk']])

    def test_func(self):
        task = Task.objects.get(id=self.kwargs.get('pk'))
        obj = task.permitted_user_set.first()

        return (
                self.request.user == task.author or
                self.request.user in obj.comment_allowed_users.all()
        )


class TaskDetailView(View):
    """ Combine `TaskDisplayDetailView` and `CommentView` """

    def get(self, request, *args, **kwargs):
        view = TaskDisplayDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentView.as_view()
        return view(request, *args, **kwargs)


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    """ View for Create a new task. """
    model = Task
    form_class = TaskForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView
):
    """ Only task owner can update the task. """
    model = Task
    fields = (
        'title',
        'description',
        'deadline',
    )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author


class TaskDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView
):
    model = Task

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author

    def get_success_url(self):
        return reverse(
            'user-tasks',
            kwargs={'username': self.request.user.username},
        )


class PermittedUsersListView(
    LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView
):
    """ Return all permitted user's list """

    template_name = 'task/permitted_users.html'

    def get_context_data(self, **kwargs):
        task = Task.objects.get(id=self.kwargs.get('pk'))
        obj = task.permitted_user_set.first()
        context = {
            'task_id': task.id,
            'comment_allowed_users': obj.comment_allowed_users.all(),
            'read_only_users': obj.read_only_users.all(),
        }
        return context

    def test_func(self):
        task = Task.objects.get(id=self.kwargs.get('pk'))
        return self.request.user == task.author


class PermittedUserUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, generic.FormView
):
    template_name = 'task/permitted_users_create_form.html'
    form_class = PermittedUserAddForm
    success_url = reverse_lazy('tasks-explore')

    def form_valid(self, form):

        # get related permitted user object
        obj = Permitted_User.objects.get(task_id=self.kwargs.get('pk'))

        # get username input data
        username = form.cleaned_data.get('username')

        # get all users in the object
        read_only_users = obj.read_only_users.all()
        comment_allowed_users = obj.comment_allowed_users.all()
        already_added_users = read_only_users | comment_allowed_users
        already_added_users = [
            each.username for each in already_added_users
        ]

        # make a list all active users in the application
        registered_users = [
            user.username
            for user in get_user_model().objects.filter(is_active=True)
        ]

        # if user is not found
        if username not in registered_users:
            form.add_error('username', _('Username is not found.'))
            return self.form_invalid(form)

        # if user has already been added
        elif username in already_added_users:
            form.add_error('username', _('This user has been already added.'))
            return self.form_invalid(form)

        new_user = get_user_model().objects.get(username=username)

        obj.read_only_users.add(new_user)
        obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        task = Task.objects.get(pk=self.kwargs['pk'])
        return self.request.user == task.author


class PermittedUserDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView
):
    model = Permitted_User
    template_name = 'task/permitted_user_confirm_delete.html'

    def get_object(self, queryset=None):
        return get_user_model().objects.get(id=self.kwargs.get('user_id'))

    def post(self, request, *args, **kwargs):
        """
        task - permitted user - user-i remove edirem

        """
        task = Task.objects.get(id=self.kwargs.get('pk'))
        permitted_users_object = task.permitted_user_set.first()
        user = get_user_model().objects.get(id=self.kwargs.get('user_id'))
        permitted_users_object.read_only_users.remove(user)
        permitted_users_object.comment_allowed_users.remove(user)
        permitted_users_object.save()
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        task = Task.objects.get(pk=self.kwargs['pk'])
        return self.request.user == task.author

    def get_success_url(self):
        return reverse('permitted-users', kwargs={'pk': self.kwargs.get('pk')})
