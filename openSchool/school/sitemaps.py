from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from school.models import *

class StaticViewSitemap(Sitemap):
    def items(self):
        return Course.objects.all()


