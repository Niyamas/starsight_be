from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PageChooserPanel, FieldRowPanel
from wagtail.api import APIField
from services.serializers import ImageURLSerializer, LinkUrlSerializer
from services.variables import image_alt_help_text, optional_button_help_text


class HomePage(Page):
	max_count = 1
	parent_page_types = ['wagtailcore.page']

	hero_image = models.ForeignKey(
    'wagtailimages.Image',
    null=True,
    blank=False,
    on_delete=models.SET_NULL,
    related_name="+"
  )

	hero_image_alt = models.CharField(
    max_length=125,
    null=True,
    blank=False,
		help_text=image_alt_help_text
  )

	content_panels = Page.content_panels + [
		MultiFieldPanel([
			FieldPanel('hero_image'),
			FieldPanel('hero_image_alt')
		], heading='Hero')
	]

	api_fields = [
		APIField('hero_image', serializer=ImageURLSerializer()),
		APIField('hero_image_alt'),
	]