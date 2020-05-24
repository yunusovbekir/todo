from django.http import HttpResponseRedirect, JsonResponse
from django.core.mail import send_mail, BadHeaderError
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views import generic
from django.urls import reverse

from .models import Contact_Message, Portfolio
from .forms import ContactMessageForm


User = get_user_model()


class IndexView(generic.TemplateView):
    template_name = 'core/home/index.html'

    def get_context_data(self, **kwargs):
        context = {
            'portfolio': Portfolio.objects.all(),
        }
        return context

# -----------------------------------------------------------------------------


class ContactView(generic.TemplateView):

    template_name = 'contact/index.html'

    def get_context_data(self, **kwargs):
        ctx = {
            'form': ContactMessageForm(),
        }
        return ctx


# -----------------------------------------------------------------------------


class ContactMessageView(generic.CreateView):
    template_name = 'contact/index.html'
    model = Contact_Message
    form_class = ContactMessageForm

    def get_success_url(self):
        return reverse('contact')

    def form_valid(self, form):
        if self.request.is_ajax():

            # get form data
            name = form.cleaned_data.get('name')
            message = form.cleaned_data.get('message')
            subject = form.cleaned_data.get('subject')
            from_email = form.cleaned_data.get('email')

            # custom message
            message = _(
                'You have a message from {name}.\n'
                'Email: {email}. \n'
                'Message:\n{message}'.format(
                    name=name,
                    email=from_email,
                    message=message,
                ))
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=from_email,
                    recipient_list=['yunusovbekir@gmail.com'],
                    fail_silently=False,
                )
                obj = form.save(commit=False)
                obj.forwarded_to_email = True
                obj.save()
                return JsonResponse({
                    'redirect_url': self.get_success_url()
                })

            except BadHeaderError:
                """ Invalid header. """
                return HttpResponseRedirect(reverse('contact'))

    def form_invalid(self, form):
        super(ContactMessageView, self).form_invalid(form)
        return JsonResponse({'info': form.errors})


# -----------------------------------------------------------------------------


class PortfolioDetailView(generic.DetailView):
    model = Portfolio
    template_name = 'portfolio-details.html'


# -----------------------------------------------------------------------------


class EmailTemplateTestView(generic.TemplateView):
    template_name = 'email-template.html'


# -----------------------------------------------------------------------------


class ErrorView(generic.TemplateView):
    template_name = '404.html'


# -----------------------------------------------------------------------------


def handler404(request, exception):
    response = render(request, "404.html", context={})
    response.status_code = 404
    return response


# -----------------------------------------------------------------------------


def handler500(request):
    response = render(request, "404.html", context={})
    response.status_code = 500
    return response
