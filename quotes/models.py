from __future__ import unicode_literals

from django.db import models

class Quote(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True, blank=True, null=True)
    timestamp = models.DateTimeField(db_column='Timestamp')
    added_by = models.CharField(db_column='AddedBy', max_length=45)
    quote = models.TextField(db_column='Quote')
    active = models.BooleanField(db_column='Active')
    score_up = models.IntegerField(db_column='ScoreUp')
    score_down = models.IntegerField(db_column='ScoreDown')

    class Meta:
        db_table = 'quotes'

