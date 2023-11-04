
from django import template
from django.conf import settings

register = template.Library()

@register.filter
def get_background_image_url(color):
    return settings.SUBJECT_COLOR_BACKGROUND_IMAGES.get(color, "")
