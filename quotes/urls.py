from django.conf.urls import patterns, url, include

from . import views

quotes = patterns('quotes',
    url(r'^$', views.QuoteList.as_view()),
)
