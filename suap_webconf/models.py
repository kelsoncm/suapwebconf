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
from django.db import models

__author__ = 'Kelson da Costa Medeiros <kelsoncm@gmail.com>'


class Sala(models.Model):
    TIPO_VIRTUAL = 'Virtual'
    TIPO_FISICA = 'Física'
    TIPO_CHOICES = (
        (TIPO_VIRTUAL, TIPO_VIRTUAL),
        (TIPO_FISICA, TIPO_FISICA)
    )

    tipo = models.CharField('Tipo de sala', choices=TIPO_CHOICES, max_length=10, null=False, blank=False)
    nome = models.CharField('Nome da sala', max_length=255, null=False, blank=False)


class Evento(models.Model):
    nome = models.CharField('Nome do evento', max_length=255, null=False, blank=False)
    data_evento = models.DateField('Data do evento', null=False)
    hora_inicio = models.TimeField('Início do evento', null=False)
    hora_termino = models.TimeField('Término do evento', null=False)
    responsavel = models.CharField('Nome responsável pelo evento', max_length=255, null=False, blank=False)
    forma_autenticacao = models.CharField('Nome responsável pelo evento', max_length=255, null=False, blank=False)
    sala = models.ForeignKey('suap_webconf.Sala', verbose_name='Sala', null=False)
