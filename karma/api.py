from rest_framework import viewsets, serializers, pagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.http import Http404

from django.db.models import Sum
from .models import Score, ScoreLog

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score

class ScoreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Access to karma for named users.
    """
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

class ScoreLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreLog
        exclude = ('id',)

class ScoreLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    History of karma modifications for named users.
    """
    queryset = ScoreLog.objects.all()
    lookup_field = 'name'
    serializer_class = ScoreLogSerializer

    def retrieve(self, request, name=None):
        queryset = self.queryset.filter(name=name)
        paginator = PageNumberPagination()

        results_page = paginator.paginate_queryset(queryset, request)
        serializer = ScoreLogSerializer(results_page)
        return paginator.get_paginated_response(serializer.data)

# Kind of silly to use a ViewSet for these, but it allows the root router
# to know about these endpoints.
class TotalsViewSet(viewsets.ViewSet):
    """
    Returns the total number of names and sum of all their scores.
    """
    permission_classes = []

    def list(self, request):
        return Response({
            # There's only one instance, so return it directly by manually
            # reversing the retrieve() url for it.
            'score': reverse('api:totals-detail', args=['score'], request=request)
        })

    def retrieve(self, request, pk=None, format=None):
        if pk == 'score':
            data = {
                'names': Score.objects.count(),
                'total': Score.objects.aggregate(Sum('score'))['score__sum'] or 0
            }
        else:
            raise Http404
        return Response(data)
