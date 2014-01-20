# -*- coding: utf-8 -*-
from django import template
from django.contrib.staticfiles.storage import staticfiles_storage

register = template.Library()

@register.simple_tag(takes_context=True)
def chui_css(context):
    css = 'chui-ios'

    if context['request'].META.has_key('HTTP_USER_AGENT'):
        user_agent = context['request'].META['HTTP_USER_AGENT']

        if user_agent.find('Android') > -1:
            css = 'chui-android'
        elif user_agent.find('Windows') > -1:
            css = 'chui-win'

    css = 'css/' + css + '-3.5.1.min.css'

    return staticfiles_storage.url(css)