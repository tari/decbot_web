from rest_framework import viewsets, serializers, pagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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

class PaginatedScoreLogSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = ScoreLogSerializer

class ScoreLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    History of karma modifications for named users.
    """
    queryset = ScoreLog.objects.all()
    lookup_field = 'name'
    serializer_class = ScoreLogSerializer

    def retrieve(self, request, name=None):
        queryset = self.queryset.filter(name=name)

        paginator = Paginator(queryset, 50)
        page = request.QUERY_PARAMS.get('page')
        try:
            log = paginator.page(page)
        except PageNotAnInteger:
            log = paginator.page(1)
        except EmptyPage:
            raise Http404

        serializer = PaginatedScoreLogSerializer(log, context={'request': request})
        return Response(serializer.data)

# Kind of silly to use a ViewSet for these, but it allows the root router
# to know about these endpoints.
class TotalsViewSet(viewsets.ViewSet):
    """
    Returns the total number of names and sum of all their scores.
    """
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
