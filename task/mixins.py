from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class PermissionRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
