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
    model = Task
    template_name = 'task/explore.html'
    context_object_name = 'tasks'
    ordering = ['-date_created']

    def get_queryset(self):
        """
        return request user's tasks and the ones request user is allowed to see
        """

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
    if request user is the owner, return all tasks
    elif request user is a guest, return only allowed tasks
    else return only a message " No task you can access "
    """

    model = Task
    template_name = 'task/user_tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Task.objects.filter(author=user).order_by('-date_created')


class TaskDisplayDetailView(
    LoginRequiredMixin, UserPassesTestMixin, generic.DetailView,
):
    model = Task
    template_name = 'task/task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        context['comments'] = Comment.objects.all()  # show comments
        context['commentform'] = CommentForm()  # show comment form
        return context

    def test_func(self):
        c_task = Task.objects.get(pk=self.kwargs['pk'])
        p_users = [user for user in
                   Permitted_User.objects.filter(task=self.kwargs['pk'])]
        print(p_users)
        # for p_user in Permitted_Users.objects.filter(task=self.kwargs['pk']):
        #     p_users.append(p_user.permitted_username)
        # if self.request.user == c_task.author:
        #     return True
        # elif self.request.user in p_users:
        #     return True
        # return False

        return self.request.user == c_task.author or self.request.user in p_users


class CommentView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'task/task_detail.html'

    def form_valid(self, form):
        form.instance.username = self.request.user
        form.instance.task_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('task-detail', args=[self.kwargs['pk']])

    # def test_func(self):
    #     c_task = Task.objects.get(pk=self.kwargs['pk'])
    #     p_users = []
    #     c_p_users = []
    #
    #     for p_user in Permitted_Users.objects.filter(task=self.kwargs['pk']):
    #         p_users.append(p_user.permitted_username)
    #         if p_user.can_comment:
    #             c_p_users.append(
    #             p_user.permitted_username)  # store those who can comment
    #
    #     if self.request.user == c_task.author:
    #         return True
    #     elif (
    #     self.request.user in p_users
    #     ) and (
    #     self.request.user in c_p_users
    #     ):  # something wrong with it
    #         return True
    #     return False


class TaskDetailView(View):

    def get(self, request, *args, **kwargs):
        view = TaskDisplayDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentView.as_view()
        return view(request, *args, **kwargs)


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView
):
    model = Task
    fields = ['title', 'description', 'deadline']

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
    success_url = '/'

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author


class PermittedUsersListView(
    LoginRequiredMixin, UserPassesTestMixin, generic.ListView
):
    model = Permitted_Users
    template_name = 'task/permitted_users.html'
    context_object_name = 'p_users'

    def get_queryset(self):
        final_query = Permitted_Users.objects.filter(
            task=self.kwargs['pk']
        ).order_by('permitted_username')
        return final_query

    def get_context_data(self, **kwargs):
        context = super(
            PermittedUsersListView, self
        ).get_context_data(**kwargs)

        # a = Permitted_Users.objects.filter(
        #     task=self.kwargs['pk']
        # ).order_by('permitted_username')
        context['task_id'] = self.kwargs['pk']
        return context

    def test_func(self):
        c_task = Task.objects.get(pk=self.kwargs['pk'])
        return self.request.user == c_task.author


class PermittedUsersCreateView(
    LoginRequiredMixin, UserPassesTestMixin, generic.CreateView
):
    model = Permitted_Users
    form_class = PermittedUsersForm

    # template_name_suffix = '_create_form'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.task_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tasks-explore')

    def test_func(self):
        task = Task.objects.get(pk=self.kwargs['pk'])
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
    model = Permitted_Users
    success_url = '/'
    template_name = 'task/permitted_user_confirm_delete.html'

    def get_object(self):
        pk = self.kwargs['pk']
        permission_pk = self.kwargs['permission_pk']
        obj = self.model.objects.filter(
            task__id=pk,
            permitted_username__id=permission_pk
        ).last()
        return obj

    def test_func(self):
        task = Task.objects.get(pk=self.kwargs['pk'])
        return self.request.user == task.author
