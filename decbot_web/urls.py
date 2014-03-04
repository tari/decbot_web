from django.conf.urls import patterns, include, url

import quotes.urls

urlpatterns = patterns('',
    url(r'^api/', include(quotes.urls.api)),
    url(r'^ns/', include(quotes.urls.noscript)),
)
