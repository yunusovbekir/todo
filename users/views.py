from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from core.models import Task

from .forms import UserRegisterForm, UserUpdateForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('tasks-explore')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


class ProfileView(
    LoginRequiredMixin, generic.TemplateView
):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        tasks = Task.objects.filter(author=self.request.user)
        context = {
            'object': get_user_model().objects.get(id=self.request.user.id),
            'form': UserUpdateForm(instance=self.request.user),
            'tasks': tasks,
            'task_count': tasks.count(),
        }
        return context


class ProfileUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView
):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('profile')

    def test_func(self):
        return self.request.user.id == self.kwargs.get('pk')
