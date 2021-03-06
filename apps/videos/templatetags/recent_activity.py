# Universal Subtitles, universalsubtitles.org
# 
# Copyright (C) 2010 Participatory Culture Foundation
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see 
# http://www.gnu.org/licenses/agpl-3.0.html.

#  Based on: http://www.djangosnippets.org/snippets/73/
#
#  Modified by Sean Reifschneider to be smarter about surrounding page
#  link context.  For usage documentation see:
#
#     http://www.tummy.com/Community/Articles/django-pagination/

from django import template
from videos.models import VideoCaptionVersion, TranslationVersion
from django.conf import settings
from datetime import date

register = template.Library()

def events_info_generator(events):
    for item in events:
        obj = {}
        if isinstance(item, TranslationVersion):
            obj['language'] = item.language.get_language_display()
            obj['video'] = item.language.video
        else:
            obj['video'] = item.video
        obj['user'] = obj['video'].owner
        if item.datetime_started.date() == date.today():
            format = '%I:%M %p'
        else:
            format = '%I:%M %p, %d %b %Y'
        obj['time'] = item.datetime_started.strftime(format)    
        yield obj

@register.inclusion_tag('videos/_recent_activity.html')
def recent_activity():
    LIMIT = settings.RECENT_ACTIVITIES_ONPAGE
    
    events = list(VideoCaptionVersion.objects.select_related().order_by('-datetime_started')[:LIMIT])
    events.extend(TranslationVersion.objects.select_related().order_by('-datetime_started')[:LIMIT])
    events.sort(key = lambda event: event.datetime_started, reverse=True)
    events = events[:LIMIT]
    
    return {
        'events': events_info_generator(events)
    }