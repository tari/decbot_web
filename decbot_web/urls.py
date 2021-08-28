from django.conf.urls import include, url
from rest_framework import routers

from karma.urls import karma, karma_log
from karma.views import ScoreSummary
from quotes.api import QuoteViewSet
from karma.api import ScoreViewSet, ScoreLogViewSet, TotalsViewSet
from spa.views import spa

router = routers.DefaultRouter(trailing_slash=False)
router.register('quotes', QuoteViewSet)
router.register('scores', ScoreViewSet)
router.register('scores-log', ScoreLogViewSet)
router.register('totals', TotalsViewSet, basename='totals')
api = ([
    url(r'^', include(router.urls)),
], 'api')

urlpatterns = [
    url(r'^$', ScoreSummary.as_view()),
    url(r'^_spa', spa, name='spa'),
    url(r'^api/', include(api, 'api')),
    url(r'^quotes/', include('quotes.urls')),
    url(r'^scores/', include(karma, 'scores')),
    url(r'^scores-log/', include(karma_log, 'scores-log')),
]
