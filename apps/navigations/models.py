from django.db import models
from django.utils.text import slugify
from wagtail.models import Orderable
from wagtail.admin.panels import (
  MultiFieldPanel,
  InlinePanel,
  FieldPanel,
  PageChooserPanel
)
from wagtail.api import APIField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from services.serializers import LinkUrlSerializer


class Links(Orderable):
  """
  Children of the Navigation model.
  """

  title = models.CharField(max_length=50, blank=False, null=True)
  page = models.ForeignKey('wagtailcore.Page', blank=True, null=True, related_name='+', on_delete=models.CASCADE, help_text="This field has priority over the Url field.")
  url = models.CharField(max_length=500, blank=True)
  open_in_new_page = models.BooleanField(default=False, blank=False, null=False)
  child_of = ParentalKey('Navigation', related_name='links')

  panels = [
    FieldPanel('title'),
    PageChooserPanel('page'),
    FieldPanel('url'),
    FieldPanel('open_in_new_page'),
  ]

  api_fields = [
    APIField('title'),
    APIField('page', serializer=LinkUrlSerializer()),
    APIField('url'),
    APIField('open_in_new_page'),
  ]

class Navigation(ClusterableModel):
  """
  Can create navigation names like header menu & footer menu,
  and their corresponding links.
  """

  title = models.CharField(max_length=100)
  slug = models.SlugField(unique=True, blank=False, null=True)

  panels = [
    MultiFieldPanel([
      FieldPanel('title'),
      FieldPanel('slug'),
    ], heading='Navigation'),
    InlinePanel('links', label='Links')                    # Referenced in Link's page ParentalKey
  ]

  api_fields = [
    APIField('title'),
    APIField('slug'),
    APIField('links'),
  ]

  def __str__(self):
    return self.title

  def save(self, *args, **kwargs):
    super(Navigation, self).save(*args, **kwargs)
    self.slug = slugify(self.title, allow_unicode=True)
    return super(Navigation, self).save(*args, **kwargs)