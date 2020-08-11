from django import template
from ..models import Like, Post

register = template.Library()

@register.simple_tag
def has_liked(user, post):
    like = Like.objects.filter(user=user, post=post).first()
    if like is not None:
        return True
    else:
        return False

