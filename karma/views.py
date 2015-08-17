from django.views.generic import ListView, DetailView
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from karma.models import Score, ScoreLog

class ScoreSummary(ListView):
    model = Score
    context_object_name = 'things'

    def get_context_data(self, **kwargs):
        context = super(ScoreSummary, self).get_context_data(**kwargs)
        total = 0
        last_score = float('inf')
        rank = 0
        for thing in context['things']:
            if thing.score < last_score:
                rank += 1
            last_score = thing.score
            thing.rank = rank
            total += thing.score

        context['total_score'] = total
        return context

class ScoreDetail(DetailView):
    model = Score

    def get_context_data(self, **kwargs):
        context = super(ScoreDetail, self).get_context_data(**kwargs)

        name = kwargs['object'].name
        last_updated = None
        qs = ScoreLog.objects.filter(name=name)
        if qs.count() > 0:
            last_updated = qs[0].timestamp

        context['log'] = qs
        context['last_updated'] = last_updated
        return context

class ScoreLogSummary(ListView):
    model = ScoreLog
    context_object_name = 'changes'

class ScoreLogDetail(ListView):
    model = ScoreLog
    template_name_suffix = '_single_list'
    context_object_name = 'changes'

    def get_queryset(self, *args, **kwargs):
        qs = ScoreLog.objects.filter(name=self.kwargs['pk'])
        if qs.count() == 0:
            raise Http404
        else:
            return qs


def score_graph(request):
    raise Http404("Static graphs are no longer supported")

def score_log_graph(request, pk=None):
    raise Http404("Static graphs are no longer supported")
