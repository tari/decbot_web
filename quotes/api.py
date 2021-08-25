from quotes.models import Quote
from quotes.serializers import QuoteSerializer

from rest_framework import viewsets
from rest_framework.response import Response


class QuoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view and edit quotes.
    """
    queryset = Quote.all_active()
    serializer_class = QuoteSerializer

    def list(self, request, *args, **kwargs):
        response = super(QuoteViewSet, self).list(request, *args, **kwargs)
        response.data = {"results": response.data}

        return response

    def vote(f):
        def vote_internal(self, request, pk=None):
            quote = self.get_object()
            f(quote)
            quote.save()

            score = quote.score_up - quote.score_down
            return Response({
                'status': 'OK',
                'score': score
            })

        return vote_internal

#    @action(permission_classes=(AllowAny,))
#    @vote
#    def upvote(quote):
#        quote.score_up += 1
#
#    @action(permission_classes=(AllowAny,))
#    @vote
#    def downvote(self, request, pk=None):
#        quote.score_down += 1
