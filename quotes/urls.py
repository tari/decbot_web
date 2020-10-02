from django.conf.urls import url, include

from . import views

quotes = (
    url(r'^$', views.QuoteList.as_view()),
    url(r'^(?P<pk>\d+)$', views.QuoteView.as_view(), name='quote_view')
)
