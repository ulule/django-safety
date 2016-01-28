# -*- coding: utf-8 -*-
from django.apps import AppConfig


class SafetyConfig(AppConfig):
    name = 'safety'
    verbose_name = 'Safety'

    def ready(self):
        super(SafetyConfig, self).ready()
