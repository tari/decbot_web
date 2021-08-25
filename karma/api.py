from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from rest_framework import viewsets, serializers, pagination
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.http import Http404

from django.db.models import Sum
from .models import Score, ScoreLog


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['name', 'score']


class ScoreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Access to karma for named users.
    """
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

    def list(self, request, *args, **kwargs):
        response = super(ScoreViewSet, self).list(request, *args, **kwargs)
        response.data = {"results": response.data}

        return response


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
    page_size = 50
    serializer_class = ScoreLogSerializer

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset.filter(name=kwargs.get('name'))

        paginator = Paginator(queryset, 50)
        page = request.query_params.get('page')
        try:
            log = paginator.page(page)
        except PageNotAnInteger:
            log = paginator.page(1)
        except EmptyPage:
            raise Http404

        return Response({
            'count': len(log.object_list),
            'next': reverse(
                'scores-log:score-log-detail', args=[log.next_page_number()]
            ) if log.has_next() else None,
            'previous': reverse(
                'scores-log:score-log-detail', args=[log.previous_page_number()]
            ) if log.has_previous() else None,
            'results': [ScoreLogSerializer(score_log).data for score_log in
                        log.object_list]
        })


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
