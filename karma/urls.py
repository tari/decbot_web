from django.conf.urls import url

from . import views

karma = ([
    url(r'^$', views.ScoreSummary.as_view(), name='score-summary'),
    url(r'^scores\.png$', views.score_graph, name='score_graph'),
    url(r'^(?P<pk>.+?)\.png', views.score_log_graph, name='score_log_graph'),
    url(r'^(?P<pk>.+)$', views.ScoreDetail.as_view(), name='score-detail'),
], 'scores')

karma_log = ([
    url(r'^$', views.ScoreLogSummary.as_view(), name='score-log-summary'),
    url(r'(?P<pk>.+?)\.png$', views.score_log_graph, name='score_log_graph'),
    url(r'(?P<pk>.+)$', views.ScoreLogDetail.as_view(), name='score-log-detail'),
], 'scores-log')
