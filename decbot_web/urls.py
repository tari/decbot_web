from django.conf.urls import patterns, include, url

from .views import noscript_redirect
import quotes.urls

urlpatterns = patterns('',
    url(r'^api/', include(quotes.urls.api)),
    url(r'^ns_redir$', noscript_redirect),
    url(r'^ns/', include(quotes.urls.noscript)),
)
