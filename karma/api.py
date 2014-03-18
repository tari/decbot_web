from rest_framework import viewsets, serializers

from .models import Score

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score

class ScoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
