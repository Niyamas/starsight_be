from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from rest_framework import serializers
from wagtail.models import Page, Orderable
from wagtail.fields import StreamField, RichTextField
from wagtail.search import index
from wagtail.admin.panels import (
  FieldPanel,
  MultiFieldPanel,
  InlinePanel
)
from wagtail.snippets.models import register_snippet
from wagtail.api import APIField
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from services.serializers import ArticleListingChildPagesSerializer, ImageURLSerializer, TotalPostNumberSerializer
from services.variables import image_alt_help_text
from apps.streamfields.blocks import (
  CustomRichTextBlock,
  DetailedImageBlock,
  ReferencesBlock,
)

class ArticleListingPage(Page):
  max_count = 1
  parent_page_types = ['home.HomePage']
  subpage_types = ['articles.ArticleDetailPage',]

  api_fields = [
    APIField('total_post_number', TotalPostNumberSerializer(source='get_total_post_number')),
    APIField('front_page_article_posts', ArticleListingChildPagesSerializer(source='get_front_page_article_posts')),
  ]

  @property
  def get_front_page_article_posts(self):
    # Use this instead of get_children() to get each page's fields
    return ArticleDetailPage.objects.child_of(self).public().live().order_by('-first_published_at')[:6]

  @property
  def get_total_post_number(self):
    return self.get_children().public().live().count()

class ArticlePageTag(TaggedItemBase):
  """
  Add tags to the ArticleDetailPage.
  """
  content_object = ParentalKey(
    'ArticleDetailPage',
    related_name='tagged_items',
    on_delete=models.CASCADE
  )

class ArticleDetailPage(Page):
  parent_page_types = ['articles.ArticleListingPage']
  subpage_types = []
  
  preview_text = RichTextField(features=['bold', 'italic'], max_length=200, null=True, blank=False)
  topic = models.ForeignKey('articles.ArticleTopic', blank=False, null=True, on_delete=models.SET_NULL)
  image = models.ForeignKey('wagtailimages.Image', blank=False, null=True, on_delete=models.SET_NULL, related_name='+')
  alt = models.CharField(max_length=125, blank=False, null=True, help_text=image_alt_help_text)
  caption = models.CharField(max_length=100, blank=True, null=True, help_text="Enter the source name for this image")
  content = StreamField([
    ('article_rich_text_block', CustomRichTextBlock()),
    ('detailed_image_block', DetailedImageBlock()),
    ('references_block', ReferencesBlock()),
  ], null=True, blank=True, use_json_field=True)
  tags = ClusterTaggableManager(through=ArticlePageTag, blank=True)
  published_date = models.DateField(blank=True, null=True, help_text="You may choose a date that's different from the first published date.")

  content_panels = Page.content_panels + [
    FieldPanel('preview_text'),
    FieldPanel('topic'),
    MultiFieldPanel([
      FieldPanel('image'),
      FieldPanel('alt'),
      FieldPanel('caption'),
    ], heading='Header Image'),
    MultiFieldPanel([
      InlinePanel('article_authors', min_num=1, max_num=3),
    ], heading='Authors', help_text="You may add 1-3 authors."),
    FieldPanel('content'),
    FieldPanel('tags'),
    FieldPanel('published_date'),
  ]

  api_fields = [
    APIField('preview_text'),
    APIField('topic', serializer=serializers.StringRelatedField(many=False)),
    APIField('image', serializer=ImageURLSerializer()),
    APIField('alt'),
    APIField('caption'),
    APIField('article_authors'),
    APIField('content'),
    APIField('tags'),
    APIField('published_date'),
  ]

@register_snippet
class ArticleTopic(models.Model):
  name = models.CharField(max_length=100, blank=False, null=True)
  slug = models.SlugField(unique=True, blank=True, null=True)

  panels = [
    FieldPanel('name'),
    FieldPanel('slug'),
  ]

  # @todo: what does this do????
  search_fields = [
    index.SearchField('name', partial_match=True),
  ]

  class Meta:
    verbose_name = 'Article Topic'
    verbose_name_plural = 'Article Topics'
    ordering = ['name']

  def __str__(self):
    """For vanilla Django to know how to name each model object created."""
    return self.name

  def save(self, *args, **kwargs):
    super(ArticleTopic, self).save(*args, **kwargs)
    self.slug = slugify(self.name, allow_unicode=True)
    return super(ArticleTopic, self).save(*args, **kwargs)

class ArticleAuthorsOrderable(Orderable):
  """
  This allows us to select one or more authors from the Snippets page,
  which can be used in the article detail pages
  """
  page = ParentalKey('articles.ArticleDetailPage', related_name='article_authors')
  author = models.ForeignKey('articles.ArticleAuthor', on_delete=models.CASCADE)

  @property
  def name(self):
    return self.author.user.first_name + ' ' + self.author.user.last_name

  @property
  def email(self):
    if self.author.add_email_link:
      return self.author.user.email
    else:
      return None

  api_fields = [
    APIField('name'),
    APIField('email'),
  ]

@register_snippet
class ArticleAuthor(models.Model):
  """
  Article author for snippets using vanilla Django models.
  """
  user = models.OneToOneField(User, blank=False, null=True, on_delete=models.CASCADE, unique=True)
  image = models.ForeignKey('wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+')
  add_email_link = models.BooleanField(default=False, help_text="You can update your email in your account settings.")
  website = models.URLField(blank=True, null=True)

  panels = [
    FieldPanel('user'),
    FieldPanel('add_email_link'),
    FieldPanel('website'),
  ]

  class Meta:
    verbose_name = 'Article Author'
    verbose_name_plural = 'Article Authors'

  def __str__(self):
    """For vanilla Django to know how to name each model object created."""
    if self.user.first_name and self.user.last_name:
      return self.user.first_name + ' ' + self.user.last_name
    else:
      return self.user.username