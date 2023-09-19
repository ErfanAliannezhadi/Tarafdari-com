from django import template

register = template.Library()


@register.inclusion_tag('posts/nested_comments.html')
def replies(comment_replies):
    return {'comments': comment_replies}
