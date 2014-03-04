from django.conf.urls import patterns, url, include
from rest_framework import routers

from . import api, views

router = routers.DefaultRouter()
router.register(r'quotes', api.QuoteViewSet)

api = patterns('api',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
        namespace='rest_framework'))
)

noscript = patterns('ns',
    url(r'^$', views.QuoteList.as_view()),
)
