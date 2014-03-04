from __future__ import unicode_literals
from django.db import models
from datetime import datetime

from datetime import datetime, timezone
now = lambda: datetime.now(timezone.utc)

class Quote(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)
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

    @property
    def lines(self):
        return self.quote.split('|')

    @classmethod
    def all_active(cls):
        return cls.objects.filter(active=True)

#class Vote(models.Model):
#    id = models.IntegerField(primary_key=True)
#    # TODO prefer composite primary key of quote ID and SID
#    #session = 
#    #quote = models.ForeignKeyField(
#
#    class Meta:
#        db_table = 'quotes_votes'
#        unique_together = ('sid', 'quote')

