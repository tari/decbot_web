from django.conf.urls import url

from . import views

app_name = 'quotes'
urlpatterns = [
    url(r'^$', views.QuoteList.as_view()),
    url(r'^(?P<pk>\d+)$', views.QuoteView.as_view(), name='quote_view')
]
