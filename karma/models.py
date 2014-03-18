from django.db import models

class Score(models.Model):
    # When creating a Score, must provide force_insert=True
    name = models.CharField(db_column='Name', max_length=100,
                            null=False, primary_key=True)
    score = models.IntegerField(db_column='Score', null=False)

    class Meta:
        db_table = 'scores'
        ordering = ['-score']

    def __unicode__(self):
        return u'{}: {}'.format(self.name, self.score)

class Link(models.Model):
    name = models.CharField(db_column='Name', max_length=100,
                            null=False, primary_key=True)
    link = models.CharField(db_column='Link', max_length=100,
                            null=False)

    class Meta:
        db_table = 'links'
