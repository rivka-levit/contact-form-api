"""
Views for endpoints that don't belong to any app.
"""

from django.views.generic import TemplateView


class IndexView(TemplateView):
    """View for index page."""

    template_name = 'index.html'

