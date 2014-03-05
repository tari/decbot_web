from quotes.models import Quote

from rest_framework import serializers

class QuoteSerializer(serializers.HyperlinkedModelSerializer):
    lines = serializers.WritableField(source='lines')

    class Meta:
        model = Quote
        fields = ('id', 'timestamp', 'added_by', 'lines')
