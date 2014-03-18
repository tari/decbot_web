from django.conf.urls import patterns, url, include

from . import views

karma = patterns('quotes',
    url(r'^$', views.ScoreSummary.as_view()),
    url(r'^scores.png$', views.score_graph),
)
