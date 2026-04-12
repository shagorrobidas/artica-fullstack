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

    for mapping in sorted_mappings:
        term_word = re.escape(mapping.term.term)
        slug = mapping.term.slug
        
        # We need to render a span tag
        replacement = f'<span class="interactive-term" data-term-slug="{slug}">\\1</span>'
        
        # Regex to match the term globally, outside of HTML tags.
        # It's a tricky regex. Simple approximation: match term only if it's not inside <...>
        # Using a negative lookahead helper.
        pattern = re.compile(rf'(?i)\b({term_word})\b(?![^<]*>)')
        
        # Handle occurrences
        if mapping.occurrence_index == 0:
            content = pattern.sub(replacement, content)
        else:
            # Replace only the nth occurrence
            # This is complex with regex. A simpler approach is to split and join or use a counter.
            # For robustness, we will just use a counter function in re.sub
            counter = [0]
            def replace_nth(match):
                counter[0] += 1
                if counter[0] == mapping.occurrence_index:
                    return f'<span class="interactive-term" data-term-slug="{slug}">{match.group(1)}</span>'
                return match.group(0)
            
            content = pattern.sub(replace_nth, content)

    return mark_safe(content)
