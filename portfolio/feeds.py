from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed

from .models import Project


class ProjectsFeed(Feed):
    feed_type = Rss201rev2Feed
    title = "Мои проекты"
    link = "/projects/"
    description = "Новые проекты в портфолио"

    def items(self):
        return Project.objects.order_by("-created_at")[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return (item.description or "")[:300]

    def item_link(self, item):
        return item.get_absolute_url()
