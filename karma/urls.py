from django.conf.urls import patterns, url, include

from . import views

karma = patterns('quotes',
    url(r'^$', views.ScoreSummary.as_view(), name='score-summary'),
    url(r'^(?P<pk>.+)$', views.ScoreDetail.as_view(), name='score-detail'),
    url(r'^scores.png$', views.score_graph),
)
