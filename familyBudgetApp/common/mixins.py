class RefererURLMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['referer_url'] = self.request.META.get('HTTP_REFERER')
        return context
