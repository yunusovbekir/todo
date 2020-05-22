from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
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


# @login_required
# def profile(request):
#     if request.method == "POST":
#         u_form = UserUpdateForm(request.POST, instance=request.user)  # error
#
#         if u_form.is_valid():
#             u_form.save()
#             messages.success(request, 'Your profile has been updated')
#             return redirect('profile')
#
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#
#     context = {
#         'u_form': u_form
#     }
#
#     return render(request, 'users/profile.html', context)


class ProfileView(
    LoginRequiredMixin, generic.TemplateView
):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        tasks = Task.objects.filter(author=self.request.user)
        context = {
            'object': get_user_model().objects.get(id=self.request.user.id),
            'tasks': tasks,
            'task_count': tasks.count(),
            'form': UserUpdateForm(instance=self.request.user)
        }
        return context
