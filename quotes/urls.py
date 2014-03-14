from django.conf.urls import patterns, url, include

from . import views

quotes = patterns('quotes',
    url(r'^$', views.QuoteList.as_view()),
    url(r'^(?P<pk>\d+)$', views.QuoteView.as_view(), name='quote_view')
)
