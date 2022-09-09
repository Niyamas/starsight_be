"""
Register Navigation Snippets Wagtail API Endpoint.

WIP @todo: Add a functional navigations API endpoint to display header and footer CMS items.

See:
https://www.google.com/search?q=wagtail+BaseAPIEndpoint&ei=C6nkYKKpMd2sqtsPjN65qAs&oq=wagtail+BaseAPIEndpoint&gs_lcp=Cgdnd3Mtd2l6EAMyBwghEAoQoAEyBQghEKsCOgcIABBHELADOgcIABCwAxBDOgoILhCwAxDIAxBDOgQIABBDOgQILhBDOgIIAEoFCDgSATFKBAhBGABQzQlYmgtgmw1oAnACeACAAWiIAbICkgEDMS4ymAEAoAEBoAECqgEHZ3dzLXdpesgBDcABAQ&sclient=gws-wiz&ved=0ahUKEwji2sGjkc_xAhVdlmoFHQxvDrUQ4dUDCA8&uact=5
https://stackoverflow.com/questions/51961999/wagtail-api-how-to-expose-snippets
https://github.com/wagtail/wagtail/tree/main/wagtail/api/v2
"""

from wagtail.api.v2.views import BaseAPIViewSet
from wagtail.api.v2.serializers import BaseSerializer

from .models import Navigation

# @todo: figure out how to output api navigations to use slug rather than pk
# See: https://wagtail.io/blog/wagtail-api-how-customize-detail-url/
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import redirect
from django.urls import reverse, path

class NavigationsAPIViewset (BaseAPIViewSet):
  """
  Defines the Navigations model API endpoints. The detail
  views can now be queried using either the pk or the slug
  of the specific Navigation object.

  Thanks to: https://wagtail.io/blog/wagtail-api-how-customize-detail-url/
  """
  
  model = Navigation
  #body_fields = ['id', 'title', 'slug',]

  def detail_view(self, request, pk=None, slug=None):
    param = pk
    if slug is not None:
      self.lookup_field = 'slug'
      param = slug
    try:
      return super().detail_view(request, param)
    except MultipleObjectsReturned:
      # Redirect to the listing view, filtered by the relevant slug
      # The router is registered with the `wagtailapi` namespace,
      # `pages` is our endpoint namespace and `listing` is the listing view url name.
      return redirect(
        reverse('wagtailapi:navigations:listing') + f'?{self.lookup_field}={param}'
      )

  @classmethod
  def get_urlpatterns(cls):
    """
    This returns a list of URL patterns for the endpoint
    """
    return [
      path('', cls.as_view({'get': 'listing_view'}), name='listing'),
      path('<int:pk>/', cls.as_view({'get': 'detail_view'}), name='detail'),
      path('<slug:slug>/', cls.as_view({'get': 'detail_view'}), name='detail'),
      path('find/', cls.as_view({'get': 'find_view'}), name='find'),
    ]