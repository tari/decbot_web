from quotes.models import Quote

from rest_framework import serializers

class LinesField(serializers.WritableField):
    """
    Serialize the db `quote` field into individual lines delimited
    by pipes.
    """
    def to_native(self, obj):
        return obj.split('|')

    def from_native(self, data):
        return '|'.join(data)

class QuoteSerializer(serializers.HyperlinkedModelSerializer):
    lines = LinesField(source='quote')

    class Meta:
        model = Quote
        fields = ('id', 'timestamp', 'added_by', 'lines')
