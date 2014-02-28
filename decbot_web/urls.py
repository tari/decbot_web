from django.conf.urls import patterns, include, url

from rest_framework import routers
from quotes import views

router = routers.DefaultRouter()
router.register(r'quotes', views.QuoteViewSet)

api = patterns('api',
    url(r'^', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')
)

urlpatterns = patterns('',
    url(r'^api/', include(api)),
)
