from django.db import models

class Score(models.Model):
    # When creating a Score, must provide force_insert=True
    name = models.CharField(db_column='Name', max_length=100,
                            null=False, primary_key=True)
    score = models.IntegerField(db_column='Score', null=False)

    class Meta:
        db_table = 'scores'
        ordering = ['-score']

    def __str__(self):
        return '{}: {}'.format(self.name, self.score)

class Link(models.Model):
    name = models.CharField(db_column='Name', max_length=100,
                            null=False, primary_key=True)
    link = models.CharField(db_column='Link', max_length=100,
                            null=False)

    class Meta:
        db_table = 'links'

    @classmethod
    def canonical_name(cls, s):
        return cls.objects.get(name=s).link

class ScoreLog(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    name = models.CharField(db_column='Name', max_length=100,
                            null=False)
    change = models.IntegerField(db_column='Change', null=False)
    timestamp = models.DateTimeField(db_column='Timestamp',
                                     null=False, auto_now_add=True)

    class Meta:
        db_table = 'scores_log'
        ordering = ['-timestamp']

    def __unicode__(self):
        return "<{}+{} @{}>".format(self.name, self.change, self.timestamp)
