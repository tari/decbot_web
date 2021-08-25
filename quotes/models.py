from __future__ import unicode_literals
from django.db import models

from django.urls import reverse

try:
    # py3k
    from datetime import datetime, timezone

    now = lambda: datetime.now(timezone.utc)
except ImportError:
    from datetime import datetime, timedelta, tzinfo


    class UTC(tzinfo):
        """UTC"""

        def utcoffset(self, dt):
            return timedelta(0)

        def tzname(self, dt):
            return "UTC"

        def dst(self, dt):
            return timedelta(0)


    utc = UTC()
    now = lambda: datetime.now(utc)


class Quote(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    timestamp = models.DateTimeField(db_column='Timestamp', default=now)
    added_by = models.CharField(db_column='AddedBy', max_length=45)
    deleted_by = models.CharField(db_column='DeletedBy', max_length=45,
                                  null=True)
    quote = models.TextField(db_column='Quote')
    active = models.BooleanField(db_column='Active', default=True)
    score_up = models.IntegerField(db_column='ScoreUp', default=0)
    score_down = models.IntegerField(db_column='ScoreDown', default=0)

    class Meta:
        db_table = 'quotes'
        ordering = ['-timestamp']

    def get_absolute_url(self):
        return reverse('quotes:quote_view', kwargs={'pk': self.id})

    @property
    def lines(self):
        start = 0
        i = 0
        q = self.quote
        while i >= 0:
            i = q.find('|', i)
            if i > 0:
                if q[i - 1] != '\\':
                    yield q[start:i].strip().replace('\\|', '|')
                    start = i = i + 1
                else:
                    i += 1
        yield q[start:].strip().replace('\\|', '|')

    @lines.setter
    def lines(self, value):
        self.quote = '|'.join(value)

    @classmethod
    def all_active(cls):
        return cls.objects.filter(active=True)

# class Vote(models.Model):
#    id = models.IntegerField(primary_key=True)
#    # TODO prefer composite primary key of quote ID and SID
#    #session = 
#    #quote = models.ForeignKeyField(
#
#    class Meta:
#        db_table = 'quotes_votes'
#        unique_together = ('sid', 'quote')
