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


from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from numpy import arange

def score_graph(request):
    scores = list(Score.objects.all()[:50])
    names = [s.name for s in scores]
    scores = [s.score for s in scores]

    fig = Figure(tight_layout=True, figsize=(18,6))
    fig.patch.set_alpha(0)
    canvas = FigureCanvasAgg(fig)
    ax = fig.add_subplot(111)
    ax.grid(True, which='both')
    ax.plot(arange(len(scores)), scores, label='Score', color='red', lw=4)
    ax.legend()
    ax.set_xticks(arange(len(scores)))
    ax.set_xticklabels(names, rotation=-90)
    ax.set_yscale('symlog', basey=10, subsy=[1,2,3,4,5,6,7,8,9])
    ax.set_title('Top 50 ($log_{10}$)')

    response = HttpResponse(content_type='image/png')
    canvas.print_png(response, transparent=True)
    return response

from matplotlib import dates
from datetime import datetime

def score_log_graph(request, pk=None):
    score = get_object_or_404(Score, name=pk).score
    log = ScoreLog.objects.filter(name=pk)

    if log.count() > 0:
        score_data = []
        time_data = []
        for change in log:
            time_data.append(dates.date2num(change.timestamp))
            score_data.append(score)
            score -= change.change
    else:
        score_data = [0, score]
        time_data = [dates.date2num(datetime(1970, 1, 1)),
                     dates.date2num(datetime.now())]

    fig = Figure(tight_layout=True, figsize=(18, 6))
    fig.patch.set_alpha(0)
    canvas = FigureCanvasAgg(fig)
    ax = fig.add_subplot(111)
    ax.grid(True, which='both')
    ax.plot(time_data, score_data, label='Score', color='red', lw=3, marker='o')
    locator = dates.AutoDateLocator()
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(dates.AutoDateFormatter(locator))
    ax.legend()
    ax.set_title('Score history for ' + pk)

    response = HttpResponse(content_type='image/png')
    canvas.print_png(response, transparent=True)
    return response
