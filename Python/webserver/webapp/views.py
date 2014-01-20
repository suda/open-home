from django.shortcuts import render_to_response
from django.template import RequestContext


def index(request):
    return render_to_response(
        'index.html',
        { 'request': request },
        context_instance=RequestContext(request)
    )

def cache_manifest(request):
    return render_to_response(
        'cache.manifest',
        {},
        context_instance=RequestContext(request),
        content_type='text/cache-manifest'
    )