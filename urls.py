from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from common import rest as common_rest

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'thegreco.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^app/$', TemplateView.as_view(template_name='common/app.html'), name="app"),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^rest/common/', include(common_rest.router.urls))
)
