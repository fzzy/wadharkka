# -*- coding: utf-8 -*-
from django.core.validators import email_re
import misaka as m

def parse_md(data):
    """Parse markdown data with misaka"""
    return m.html(
        data,
        extensions=m.EXT_STRIKETHROUGH|m.EXT_SUPERSCRIPT|m.EXT_TABLES|m.EXT_FENCED_CODE|m.EXT_AUTOLINK,
        render_flags=m.HTML_SKIP_HTML|m.HTML_TOC|m.HTML_SAFELINK)

def validate_email(email):
    """Return True on valid given email address, otherwise False"""
    if email_re.match(email):
        return True
    return False
