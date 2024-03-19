from django.views import generic as views


# Create your views here.
class IndexView(views.TemplateView):
    template_name = 'web/index.html'


class AboutView(views.TemplateView):
    template_name = 'web/about.html'