from builtins import getattr, super

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import (
                            ListView,
                            DetailView,
                            CreateView,
                            UpdateView,
                            DeleteView,
)
from queryset_sequence import QuerySetSequence
from .models import *
from .forms import *


class TaskListView(ListView):
    model = Task
    template_name = 'task/explore.html'   #<app>/<model>_<viewtype>.html
    context_object_name = 'tasks'
    ordering = ['-date_created']

    def get_queryset(self):
        logged_user = self.request.user
        user = User.objects.filter(username = logged_user)
        tasks = Permitted_Users.objects.filter(permitted_username__in = user).values('task')
        query1 = Task.objects.filter(id__in = tasks)
        query2 = Task.objects.filter(author__in = user) #returns only logged user's tasks
        return QuerySetSequence(query1, query2)


class UserTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task/user_tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Task.objects.filter(author=user).order_by('-date_created')


class TaskDisplayDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Task
    template_name = 'task/task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        context['comments'] = Comment.objects.all()  #show comments
        context['commentform'] = CommentForm()       #show comment form
        return context

    def test_func(self):
        c_task = Task.objects.get(pk=self.kwargs['pk'])
        p_users = []
        for p_user in Permitted_Users.objects.filter(task=self.kwargs['pk']):
            p_users.append(p_user.permitted_username)
        if self.request.user == c_task.author:
            return True
        elif self.request.user in p_users:
            return True
        return False


class CommentView(LoginRequiredMixin, CreateView):
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
    #             c_p_users.append(p_user.permitted_username) #store those who can comment
    #
    #     if self.request.user == c_task.author:
    #         return True
    #     elif (self.request.user in p_users) and (self.request.user in c_p_users): #something wrong with it
    #         return True
    #     return False


class TaskDetailView(View):

    def get(self, request, *args, **kwargs):
        view = TaskDisplayDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentView.as_view()
        return view(request, *args, **kwargs)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = MyForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'deadline']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        Task = self.get_object()
        if self.request.user == Task.author:
            return True
        return False


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    success_url = '/'

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.author:
            return True
        return False


class PermittedUsersListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Permitted_Users
    template_name = 'task/permitted_users.html'
    context_object_name = 'p_users'

    def get_queryset(self):
        final_query = Permitted_Users.objects.filter(task=self.kwargs['pk']).order_by('permitted_username')
        return final_query

    def get_context_data(self, **kwargs):
        context = super(PermittedUsersListView, self).get_context_data(**kwargs)
        a = Permitted_Users.objects.filter(task=self.kwargs['pk']).order_by('permitted_username')
        context['task_id'] = self.kwargs['pk']
        return context

    def test_func(self):
        c_task = Task.objects.get(pk=self.kwargs['pk'])
        if self.request.user == c_task.author:
            return True
        return False


class PermittedUsersCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Permitted_Users
    form_class = PermittedUsersForm
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.task_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tasks-explore')

    def test_func(self):
        task = Task.objects.get(pk=self.kwargs['pk'])
        if self.request.user == task.author:
            return True
        return False


class PermittedUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Permitted_Users
    success_url = '/'
    template_name = 'task/permitted_user_confirm_delete.html'

    def get_object(self):
        pk = self.kwargs['pk']
        permission_pk = self.kwargs['permission_pk']
        obj = self.model.objects.filter(task__id = pk, permitted_username__id = permission_pk).last()
        return obj

    def test_func(self):
        task = Task.objects.get(pk=self.kwargs['pk'])
        if self.request.user == task.author:
            return True
        return False
