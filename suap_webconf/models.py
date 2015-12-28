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
    TIPO_RNP = 'RNP'
    TIPO_POLYCON = 'PolyCon'
    TIPO_CHOICES = (
        (TIPO_RNP, TIPO_RNP),
        (TIPO_POLYCON, TIPO_POLYCON)
    )

    tipo = models.CharField('Tipo de sala', choices=TIPO_CHOICES, max_length=10, null=False, blank=False)
    nome = models.CharField('Nome da sala', max_length=255, null=False, blank=False)

    class Meta:
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'

    def __str__(self):
        return "%s (%s)" % (self.nome, self.tipo)

    def __unicode__(self):
        return "%s (%s)" % (self.nome, self.tipo)


class Evento(models.Model):
    # AUTENTICACAO_LDAP = 'LDAP'
    AUTENTICACAO_SUAP = 'SUAP'
    AUTENTICACAO_MANUAL = 'Manual'
    AUTENTICACAO_ANONIMO = 'Anonimo'
    AUTENTICACAO_CHOICES = (
        # (AUTENTICACAO_LDAP, AUTENTICACAO_LDAP),
        (AUTENTICACAO_SUAP, AUTENTICACAO_SUAP),
        (AUTENTICACAO_MANUAL, AUTENTICACAO_MANUAL),
        (AUTENTICACAO_ANONIMO, AUTENTICACAO_ANONIMO),
    )

    nome = models.CharField('Nome do evento', max_length=255, null=False, blank=False)
    data_evento = models.DateField('Data', null=False)
    hora_inicio = models.TimeField('Hora de início', null=False)
    hora_termino = models.TimeField('Hora de término', null=False)
    responsavel = models.CharField('Nome responsável', max_length=255, null=False, blank=False)
    forma_autenticacao = models.CharField('Forma de autenticação', choices=AUTENTICACAO_CHOICES, max_length=10, null=False, blank=False)
    sala = models.ForeignKey(Sala, verbose_name='Sala', null=False)

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'

    def __unicode__(self):
        return "%s @ %s(%s) - %s %s/%s" % \
               (self.nome, self.sala, self.forma_autenticacao, self.data_evento, self.hora_inicio, self.hora_termino, )


class Participante(models.Model):
    evento = models.ForeignKey(Evento, verbose_name='Evento', null=False)
    nome = models.CharField('Nome completo', max_length=255, null=False, blank=False)
    username = models.CharField('Nome do usuário', max_length=255, null=False, blank=False)
    password = models.CharField('Senha', max_length=255, null=True, blank=True)
    email = models.CharField('Email', max_length=255, null=True, blank=True)
    celular = models.CharField('Celular', max_length=255, null=True, blank=True)

    def __unicode__(self):
        return "%s EVENT: %s" % (self.nome, self.evento, )


class Acesso(models.Model):
    participante = models.ForeignKey(Participante, verbose_name='Participante', null=False)
    quando = models.DateTimeField('Quando', null=False)

    def __unicode__(self):
        return "%s %s" % (self.participante, self.quando, )

