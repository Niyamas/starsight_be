from wagtail.blocks import (
  CharBlock,
  ListBlock,
  RichTextBlock,
  StructBlock,
  URLBlock,
)
from wagtail.images.blocks import ImageChooserBlock
from wagtail.templatetags.wagtailcore_tags import richtext
from services.variables import (
  image_alt_help_text,
  simple_richtext_features
)

class CustomRichTextBlock(RichTextBlock):
  
  class Meta:
    icon = 'doc-full'
    label = 'Rich Text Block'
    help_text = 'Add free-form text content on a page, with a variety of tools like creating headings and bolding text.'

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.features = simple_richtext_features

  def get_api_representation(self, value, context=None):
    return richtext(value.source)

class DetailedImageBlock(StructBlock):
  title = CharBlock(max_length=70, required=False)
  image = ImageChooserBlock(required=True)
  image_alt = CharBlock(max_length=125, required=True, help_text=image_alt_help_text)
  caption = CharBlock(max_length=150, required=False)

  class Meta:
    icon = 'image'
    label = 'Image Block'
    help_text = 'Adds an image with optional title and caption.'


  def get_api_representation(self, value, context=None):
    return {
      'title': value.get('title'),
      'image': value.get('image').file.url,
      'alt': value.get('image_alt'),
      'caption': value.get('caption'),
    }

class ReferencesBlock(StructBlock):

  references = ListBlock(
    StructBlock([
      ('reference', CharBlock(required=True, help_text='For APA-style references, visit: https://www.citationmachine.net/apa')),
      ('url', URLBlock(required=False))
    ], icon = 'link')
  )

  class Meta:
    icon = 'doc-full'
    label = 'References Block'