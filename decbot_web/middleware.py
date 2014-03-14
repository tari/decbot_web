import re
from django.http import HttpResponseRedirect

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

# Must not rewrite API endpoints or the noscript redirect handler.
NS_EXCLUSIONS = re.compile('^/(ns_redir$|api)')

class AJAXCookieMiddleware(object):
    def process_request(self, request):
        # Do nothing if path is excluded
        if NS_EXCLUSIONS.match(request.path_info):
            return

        interface = 'noscript'
        try:
            interface = request.COOKIES['interface']
        except KeyError:
            pass

        # If cookie says to use AJAX, internal redirect. Otherwise be
        # conservative and use the script-free version.
        if interface == 'ajax':
            rpath = urlencode({
                'redirect_src': request.path_info
            })
            return HttpResponseRedirect('/static/index.html?' + rpath)
        else:
            # TODO might be more reasonable to only do this rewrite if the path
            # doesn't resolve.
            request.path_info = '/ns' + request.path
        #request.path = request.path_info
