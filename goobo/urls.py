from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'goobo.views.home', name='home'),
    url(r'^goobo/$', 'main.views.goobo_control_panel', name='goobo_control_panel'),
    url(r'^goobo/say/$', 'main.views.goobo_say', name='goobo_say'),
    url(r'^goobo/start/$', 'main.views.goobo_start', name='goobo_start'),
    url(r'^goobo/restart/$', 'main.views.goobo_restart', name='goobo_restart'),
    url(r'^goobo/quit/$', 'main.views.goobo_quit', name='goobo_quit'),
    # url(r'^goobo/', include('goobo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
