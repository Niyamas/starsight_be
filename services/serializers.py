from wagtail.core.templatetags.wagtailcore_tags import richtext
from rest_framework.fields import Field
from rest_framework.serializers import ChoiceField

class ImageURLSerializer(Field):
  def to_representation(self, image):
    return image.file.url

class LinkUrlSerializer(Field):
  def to_representation(self, page):
    return page.url

class TypeChoiceSerializer(ChoiceField):
  """
  See: https://stackoverflow.com/questions/28945327/django-rest-framework-with-choicefield
  """
  def to_representation(self, value):
    if value == '' and self.allow_blank:
      return value
    return self._choices[value]

  def to_internal_value(self, data):
    # To support inserts with the value
    if data == '' and self.allow_blank:
      return ''

    for key, val in self._choices.items():
      if val == data:
        return key
    self.fail('invalid_choice', input=data)

class ArticleListingChildPagesSerializer(Field):
  def to_representation(self, child_pages):
    return [
      {
        'id': page.id,
        'meta': {
          'html_url': page.url,
          'first_published_at': page.first_published_at,
        },
        'title': page.title,
        'preview_text': page.preview_text,
        'image': page.image.file.url,
        'alt': page.alt,
        'topic': page.topic.name,
      } for page in child_pages
    ]

class TotalPostNumberSerializer(Field):
  def to_representation(self, value):
    return value