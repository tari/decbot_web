from rest_framework import viewsets, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.http import Http404

from django.db.models import Sum
from .models import Score

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score

class ScoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

# Kind of silly to use a ViewSet for these, but it allows the root router
# to know about these endpoints.
class TotalsViewSet(viewsets.ViewSet):
    permission_classes = []

    def list(self, request):
        return Response({
            # Ick. Oh well.
            'score': reverse('totals-detail', args=['score'], request=request)
        })

    def retrieve(self, request, pk=None):
        if pk == 'score':
            data = {
                'names': Score.objects.count(),
                'total': Score.objects.aggregate(Sum('score'))['score__sum']
            }
        else:
            raise Http404
        return Response(data)
