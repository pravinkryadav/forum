"""
Default post formatting module which uses Markdown to format posts.

TODO Add a setting which points at the post formatting module to use.
"""
import re

from django.utils.html import escape
from markdown import markdown

quote_post_re = re.compile(r'^', re.MULTILINE)

def format_post_body(body):
    """
    Formats the given raw post body as HTML.
    """
    return markdown(body, safe_mode=True).strip()

def quote_post(post):
    """
    Returns a raw post body which quotes the given raw post body.
    """
    return u'**%s** [wrote](%s "View quoted post"):\n\n%s\n\n' % (
        escape(post.user.username),
        post.get_absolute_url(),
        quote_post_re.sub('> ', post.body)
    )