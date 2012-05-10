# -*- coding: utf-8 -*-
import misaka as m

def parse_md(data):
    """Parse markdown data with misaka"""
    return m.html(
        data,
        extensions=m.EXT_STRIKETHROUGH|m.EXT_SUPERSCRIPT|m.EXT_TABLES|m.EXT_FENCED_CODE|m.EXT_AUTOLINK,
        render_flags=m.HTML_SKIP_HTML|m.HTML_TOC|m.HTML_SAFELINK)
