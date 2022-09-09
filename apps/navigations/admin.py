from wagtail.contrib.modeladmin.options import (
  ModelAdmin,
  modeladmin_register
)
from .models import Navigation

# Adding extra icons: https://groups.google.com/g/wagtail/c/i3aUpnOkL6U?pli=1
# https://docs.wagtail.io/en/latest/reference/hooks.html?highlight=insert_editor_css

class NavigationAdmin(ModelAdmin):
  model = Navigation
  menu_label = 'Navigations'
  menu_icon = 'form'                    
  add_to_settings_menu = False
  exclude_from_explorer = False
  list_display = ('title', 'slug',)
  search_fields = ('title', 'slug',)

modeladmin_register(NavigationAdmin)