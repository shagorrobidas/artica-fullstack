import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def highlight_terms(content, term_mappings):
    """
    Highlights terms in the content based on the provided term_mappings.
    Replaces terms outside of HTML tags with a responsive span element.
    """
    if not content or not term_mappings:
        return content

    # Sort mappings by term length descending so longer phrases are matched first
    sorted_mappings = sorted(term_mappings, key=lambda m: len(m.term.term), reverse=True)

    # Icon mapping based on content type
    ICON_MAPPING = {
        'text': 'bx-search-alt',
        'image': 'bx-image',
        'audio': 'bx-headphone',
        'video': 'bx-video',
    }

    for mapping in sorted_mappings:
        term_word = re.escape(mapping.term.term)
        slug = mapping.term.slug
        c_type = mapping.term.content_type
        icon_class = ICON_MAPPING.get(c_type, 'bx-search-alt')
        
        # We need to render a span tag with an icon
        # The icon also gets the search icon as per user's screenshot
        icons_html = f'<i class="bx {icon_class}"></i>'
        if c_type != 'text':
             icons_html += ' <i class="bx bx-search-alt small"></i>'
        
        replacement = f'<span class="interactive-term" data-term-slug="{slug}">\\1 {icons_html}</span>'
        
        # Regex to match the term globally, outside of HTML tags.
        # \b doesn't work well with non-ASCII characters in many python versions.
        # We'll use a better approach: match term only if it's not inside <...>
        # And we use word boundaries equivalent or just the term if it's unique enough.
        # For Bangla, we might need to handle it without \b or with specific Lookbehind/Lookahead.
        pattern = re.compile(rf'(?i)({term_word})(?![^<]*>)')
        
        # Handle occurrences
        if mapping.occurrence_index == 0:
            content = pattern.sub(replacement, content)
        else:
            counter = [0]
            def replace_nth(match):
                counter[0] += 1
                if counter[0] == mapping.occurrence_index:
                    return f'<span class="interactive-term" data-term-slug="{slug}">{match.group(1)} {icons_html}</span>'
                return match.group(0)
            
            content = pattern.sub(replace_nth, content)

    return mark_safe(content)
