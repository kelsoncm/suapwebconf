# -*- coding: utf-8 -*-
"""
The MIT License (MIT)

Copyright 2015 Umbrella Tech.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from django.shortcuts import render_to_response
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from suap_webconf.models import Sala, Evento, Participante, Acesso
from suap_webconf.forms import ParticipanteAnonimoForm, ParticipanteManualForm


__author__ = 'Kelson da Costa Medeiros <kelsoncm@gmail.com>'


def _redirect_to_webconf(participante):
    participante.save()
    Acesso.objects.create(participante=participante, quando=timezone.now())
    if participante.evento.sala.tipo == Sala.TIPO_RNP:
        # TODO Redirecionar para RNP
        return redirect('http://www.google.com?q=RNP %s' % participante.username)
    if participante.evento.sala.tipo == Sala.TIPO_POLYCON:
        # TODO Redirecionar para Polycon
        return redirect('http://www.google.com?q=POLYCON %s' % participante.username)


def _user_to_participante(evento, user):
    if user.is_authenticated():
        participante = Participante.objects.filter(evento=evento, username=user.username).first()
        if participante:
            return participante
        else:
            return Participante(evento=evento,
                                nome=user.get_full_name(),
                                username=user.username,
                                email=user.email,
                                password=u'',
                                identificacao=user.username,
                                celular=u'')
    else:
        return Participante()


def webconf_index(request):
    eventos_hoje = Evento.objects.filter(data_evento=timezone.now())
    return render_to_response('webconf/index.html', locals())


def webconf_acessar(request, id):
    evento = get_object_or_404(Evento, pk=id)
    if evento.data_evento != timezone.datetime.today().date():
        raise Exception(u'O evento não será realizado hoje.')

    if request.method == "POST":
        participante = None
        if evento.forma_autenticacao == evento.AUTENTICACAO_SUAP:
            raise Exception(u'Erro, não deveria ter POST em autenticação do tipo SUAP.')
        elif evento.forma_autenticacao == evento.AUTENTICACAO_ANONIMO:
            if request.POST.get('use', None) == 'suap' and request.user.is_authenticated():
                return _redirect_to_webconf(_user_to_participante(evento, request.user))
            form = ParticipanteAnonimoForm(request.POST)
            form.instance.evento = evento
            if form.is_valid():
                participante = Participante.objects.filter(evento=evento,
                                                           nome=form.instance.nome,
                                                           username=form.instance.username).first()
                if participante:
                    participante.email = form.instance.email
                    participante.celular = form.instance.celular
                    participante.save()
                else:
                    participante = form.instance
                return _redirect_to_webconf(participante)
            return render_to_response('webconf/anonimo.html', locals(), context_instance=RequestContext(request))
        elif evento.forma_autenticacao == evento.AUTENTICACAO_MANUAL:
            form = ParticipanteManualForm(request.POST)
            form.instance = Participante(evento=evento)
            if form.is_valid():
                return _redirect_to_webconf(form.get_participante())
            else:
                return render_to_response('webconf/manual.html', locals(), context_instance=RequestContext(request))
        else:
            raise Exception(u'Não implementado.')
    else:
        participante = None
        if evento.forma_autenticacao == evento.AUTENTICACAO_SUAP:
            if request.user.is_authenticated():
                return _redirect_to_webconf(_user_to_participante(evento, request.user))
            return redirect(reverse('admin:login') + '?next=/webconf/%s/' % id)
        elif evento.forma_autenticacao == evento.AUTENTICACAO_ANONIMO:
            form = ParticipanteAnonimoForm(instance=_user_to_participante(evento, request.user))
            return render_to_response('webconf/anonimo.html', locals(), context_instance=RequestContext(request))
        elif evento.forma_autenticacao == evento.AUTENTICACAO_MANUAL:
            participante = Participante.objects.filter(evento=evento, username=request.user.username).first()
            if participante:
                return _redirect_to_webconf(participante)
            form = ParticipanteManualForm(instance=Participante(evento=evento))
            return render_to_response('webconf/manual.html', locals(), context_instance=RequestContext(request))
        else:
            raise Exception(u'Não implementado.')
