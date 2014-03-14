from django.conf.urls import patterns, include, url
from rest_framework import routers

from quotes.api import QuoteViewSet

router = routers.DefaultRouter()
router.register('quotes', QuoteViewSet)
api = patterns('api',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
        namespace='rest_framework'))
)

from quotes.urls import quotes
from quotes.views import QuoteList

urlpatterns = patterns('',
    url(r'^$', QuoteList.as_view()),
    url(r'^api/', include(api)),
    url(r'^quotes/', include(quotes)),
)
