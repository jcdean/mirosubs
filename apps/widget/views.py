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

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.sites.models import Site
from django.template import RequestContext
from videos import models
from widget.srt_subs import captions_and_translations_to_srt, captions_to_srt
import simplejson as json
from widget import rpc as rpc_views
import widget

def embed(request):
    if 'video_id' in request.GET:
        video = models.Video.objects.get(video_id=request.GET['video_id'])
    elif 'youtube_videoid' in request.GET:
        youtube_videoid = request.GET['youtube_videoid']
        try:
            video = models.Video.objects.get(youtube_videoid=youtube_videoid)
        except models.Video.DoesNotExist:
            video = models.Video(video_type=models.VIDEO_TYPE_YOUTUBE,
                                 youtube_videoid=youtube_videoid,
                                 allow_community_edits=False)
            video.save()
    else:
        video_url = request.GET['video_url']
        try:
            video = models.Video.objects.get(video_url=video_url)
        except models.Video.DoesNotExist:
            video = models.Video(video_type=models.VIDEO_TYPE_HTML5,
                                 video_url=video_url,
                                 allow_community_edits=False)
            video.save()
    video.widget_views_count += 1
    video.save()
    
    null_widget = 'null' in request.GET
    debug_js = 'debug_js' in request.GET
    if 'element_id' in request.GET:
        element_id = request.GET['element_id']
    else:
        element_id = None
    if 'autoplay' in request.GET:
        autoplay = request.GET['autoplay']
    else:
        autoplay = None
    return render_to_response('widget/embed.js', 
                              widget.js_context(request, video, 
                                                null_widget, element_id, 
                                                debug_js, autoplay),
                              mimetype="text/javascript",
                              context_instance = RequestContext(request))

def srt(request):
    video = models.Video.objects.get(video_id=request.GET['video_id'])
    if 'lang_code' in request.GET:
        lang_code = request.GET['lang_code']
        response_text = captions_and_translations_to_srt(
            video.captions_and_translations(lang_code))
    else:
        response_text = captions_to_srt(
            list(video.captions().videocaption_set.all()))
    response = HttpResponse(response_text, mimetype="text/plain")
    response['Content-Disposition'] = \
        'attachment; filename={0}'.format(video.srt_filename)
    return response

def null_srt(request):
    # FIXME: possibly note duplication with srt, and fix that.
    video = models.Video.objects.get(video_id=request.GET['video_id'])
    if 'lang_code' in request.GET:
        lang_code = request.GET['lang_code']
        response_text = captions_and_translations_to_srt(
            video.null_captions_and_translations(request.user, lang_code))
    else:
        response_text = captions_to_srt(
            list(video.null_captions(request.user).videocaption_set.all()))
    response = HttpResponse(response_text, mimetype="text/plain")
    response['Content-Disposition'] = \
        'attachment; filename={0}'.format(video.srt_filename)
    return response

def rpc(request, method_name):
    args = { 'request': request }
    for k, v in request.POST.items():
        args[k.encode('ascii')] = json.loads(v)
    func = getattr(rpc_views, method_name)
    result = func(**args)
    return HttpResponse(json.dumps(result), "application/json")

def xd_rpc(request, method_name):
    args = { 'request' : request }
    for k, v in request.POST.items():
        if k[0:4] == 'xdp:':
            args[k[4:].encode('ascii')] = json.loads(v)
    func = getattr(rpc_views, method_name)
    result = func(**args)
    params = {
        'request_id' : request.POST['xdpe:request-id'],
        'dummy_uri' : request.POST['xdpe:dummy-uri'],
        'response_json' : json.dumps(result) }
    return render_to_response('widget/xd_rpc_response.html',
                              widget.add_js_files(params))
