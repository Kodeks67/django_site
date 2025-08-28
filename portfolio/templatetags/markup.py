import bleach
import markdown as md
from django import template

register = template.Library()

ALLOWED_TAGS = [
    "p",
    "ul",
    "ol",
    "li",
    "a",
    "strong",
    "em",
    "code",
    "pre",
    "blockquote",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "img",
    "hr",
    "br",
]
ALLOWED_ATTRS = {
    "*": ["class"],
    "a": ["href", "title", "rel", "target"],
    "img": ["src", "alt", "title"],
}
ALLOWED_PROTOCOLS = ["http", "https", "mailto"]


@register.filter
def markdown_safe(value: str) -> str:
    if not value:
        return ""
    html = md.markdown(value, extensions=["extra", "codehilite"])
    cleaned = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )
    return bleach.linkify(cleaned)
