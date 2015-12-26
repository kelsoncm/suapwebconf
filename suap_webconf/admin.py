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
from __future__ import unicode_literals
from django.contrib import admin
from django.utils.html import format_html
from suap_webconf.models import Sala, Evento, Participante, Acesso

__author__ = 'Kelson da Costa Medeiros <kelsoncm@gmail.com>'


class SalaAdmin(admin.ModelAdmin):
    pass


class ParticipanteInline(admin.TabularInline):
    model = Participante


class EventoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'sala', 'data_evento', 'hora_inicio', 'hora_termino', 'responsavel', 'forma_autenticacao',
                    'show_url', ]
    inlines = [ParticipanteInline, ]

    def show_url(self, obj):
        return format_html("<a href='/admin/suap_webconf/participante/?evento__nome={nome}'>Gerenciar participantes</a>", nome=obj.nome)

    show_url.allow_tags = True


class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'evento', 'login', 'identificacao', 'email', 'celular', ]
    list_filter = ('evento__nome', )

    def show_url(self, obj):
        return format_html("<a href='/admin/participantes/{id}/'>Gerenciar participantes</a>", id=obj.id)


class AcessoAdmin(admin.ModelAdmin):
    list_display = ['participante', 'quando', ]
    list_filter = ('participante__id', )


admin.site.register(Sala, SalaAdmin)
admin.site.register(Evento, EventoAdmin)
admin.site.register(Participante, ParticipanteAdmin)
admin.site.register(Acesso, AcessoAdmin)
