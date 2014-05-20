from django.conf.urls import patterns, include, url
from rest_framework import routers

from quotes.api import QuoteViewSet
from karma.api import ScoreViewSet, TotalsViewSet

router = routers.DefaultRouter()
router.register('quotes', QuoteViewSet)
router.register('scores', ScoreViewSet)
router.register('totals', TotalsViewSet, base_name='totals')
api = patterns('api',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
        namespace='rest_framework'))
)

from quotes.urls import quotes
from karma.urls import karma
from karma.views import ScoreSummary

urlpatterns = patterns('',
    url(r'^$', ScoreSummary.as_view()),
    url(r'^api/', include(api)),
    url(r'^quotes/', include(quotes)),
    url(r'^scores/', include(karma)),
)
