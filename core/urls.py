from django.urls import path
from .views import (
    IndexView,
    ContactView,
    ContactMessageView,
    EmailTemplateTestView,
    ErrorView,
    PortfolioDetailView,
)


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('email/', EmailTemplateTestView.as_view(), name='email'),
    path('error/', ErrorView.as_view(), name='error'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact-form/', ContactMessageView.as_view(), name='contact-form'),
    path('portfolio/<int:pk>/', PortfolioDetailView.as_view(),
         name='portfolio'),
]
