from quotes.models import Quote

from django.views.generic import ListView, DetailView


class QuoteList(ListView):
    context_object_name = 'quotes'
    queryset = Quote.all_active()
    paginate_by = 50

    # TODO allow admins to view inactive quotes
    # def get_queryset(self):
    #    if self.request.user.is_admin(): return Quote.objects.all()
    #    return self.queryset


class QuoteView(DetailView):
    context_object_name = 'quote'
    queryset = Quote.all_active()
