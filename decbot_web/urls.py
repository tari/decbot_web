from django.conf.urls import include, url
from rest_framework import routers

from quotes.api import QuoteViewSet
from karma.api import ScoreViewSet, ScoreLogViewSet, TotalsViewSet

router = routers.DefaultRouter()
router.register('quotes', QuoteViewSet)
router.register('scores', ScoreViewSet)
router.register('scores-log', ScoreLogViewSet)
router.register('totals', TotalsViewSet, basename='totals')
api = (
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
        namespace='rest_framework'))
)

from quotes.urls import quotes
from karma.urls import karma, karma_log
from karma.views import ScoreSummary

urlpatterns = (
    url(r'^$', ScoreSummary.as_view()),
    url(r'^api/', include((api, 'api'))),
    url(r'^quotes/', include((quotes, 'quotes'))),
    url(r'^scores/', include((karma, 'scores'))),
    url(r'^scores-log/', include((karma_log, 'scores-log'))),
)
