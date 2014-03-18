from django.views.generic import ListView
from django.http import HttpResponse
from karma.models import Score

class ScoreSummary(ListView):
    model = Score
    context_object_name = 'things'

import matplotlib.pyplot as plt
from numpy import arange
from tempfile import SpooledTemporaryFile

def score_graph(request):
    scores = list(Score.objects.all()[:50])
    names = [s.name for s in scores]
    scores = [s.score for s in scores]

    fig = plt.figure()
    # fig.tight_layout()
    ax = fig.add_subplot(111)
    ax.grid(True, which='both')
    ax.tick_params(axis='y', labelsize=8)
    ax.tick_params(axis='x', labelsize=10)
    ax.plot(arange(len(scores)), scores, label='Score', color='red', lw=4)
    ax.legend()
    ax.set_xticks(arange(len(scores)))
    ax.set_xticklabels(names, rotation=-90)
    ax.set_yscale('symlog', basey=10, subsy=[1,2,3,4,5,6,7,8,9])
    ax.set_title('Top 50 ($log_{10}$)')

    response = HttpResponse(content_type='image/png')
    fig.savefig(response, format='png', bbox_inches='tight')
    # matplotlib requires that we explicitly close all figures
    plt.close(fig)
    return response
