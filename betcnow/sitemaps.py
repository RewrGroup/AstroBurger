from django.core.urlresolvers import reverse
from django.contrib.sitemaps import Sitemap


class ViewSitemap(Sitemap):

    def items(self):
        # Return list of url names for views to include in sitemap
        return ['home', 'play', 'membership', 'about', 'testimonios', 'results']

    def location(self, item):
        return reverse(item)