# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.core.paginator import Paginator

from django.utils.timezone import now
from safety.models import Session


class Command(BaseCommand):
    def handle(self, *args, **options):
        Session.objects.filter(expire_date__lt=now()).delete()
        self.stdout.write(self.style.SUCCESS('Deleted expired sessions'))
