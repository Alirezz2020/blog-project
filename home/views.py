
from django.views.generic import TemplateView

class LandingPageView(TemplateView):
    template_name = 'home/landing.html'
