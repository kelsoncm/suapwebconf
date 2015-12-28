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
from django.forms import ModelForm
from django.forms import CharField
from django.forms import PasswordInput
from suap_webconf.models import Participante


__author__ = 'Kelson da Costa Medeiros <kelsoncm@gmail.com>'


class ParticipanteAnonimoForm(ModelForm):

    username = CharField(label='CPF/Matricula')

    class Meta:
        model = Participante
        fields = ['nome', 'username', 'email', 'celular', ]
        hidden_fields = ['evento']


class ParticipanteManualForm(ModelForm):

    password = CharField(widget=PasswordInput)

    class Meta:
        model = Participante
        fields = ['username', 'password', ]
        hidden_fields = ['evento']

    def get_participante(self):
        return Participante.objects.filter(evento=self.instance.evento,
                                           username=self.data['username'],
                                           password=self.data['password']).first()

    def is_valid(self):
        if super(ParticipanteManualForm, self).is_valid():
            if self.get_participante():
                return True
            else:
                self.add_error(None, 'O usuário e/ou a senha estão errados.')
                return False
        else:
            return False
