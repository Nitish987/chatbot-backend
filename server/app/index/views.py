from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'views/index/home.html'

class AboutView(TemplateView):
    template_name = 'views/index/about.html'

class ContactView(TemplateView):
    template_name = 'views/index/contact.html'

class PricingView(TemplateView):
    template_name = 'views/index/pricing.html'

class ChatbotsView(TemplateView):
    template_name = 'views/index/chatbots.html'

class EmFormsView(TemplateView):
    template_name = 'views/index/emforms.html'

class DocsView(TemplateView):
    template_name = 'views/index/docs.html'

class PrivacyView(TemplateView):
    template_name = 'views/index/privacy.html'

class TermsView(TemplateView):
    template_name = 'views/index/terms.html'
