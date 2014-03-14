from datetime import datetime
from django.http import HttpResponse

try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit

def noscript_redirect(request):
    response = HttpResponse()
    response.status_code = 302
    # Clear interface cookie
    response.set_cookie('interface', 'noscript')
    
    # Redirect to the referer if provided
    # TODO need some way to check redirect loops and halt them (some cookie
    # setting to inhibit redirect, probably).
    redirect_to = '/'
    if 'HTTP_REFERER' in request.META:
        redirect_to = request.META['HTTP_REFERER']
        # Strip scheme and netloc so we always redirect to our domain.
        # TODO may need to preserve query
        redirect_to = urlsplit(redirect_to).path
    print(redirect_to)
    response['Location'] = redirect_to

    response.content = "This path is not intended for external use."
    return response
