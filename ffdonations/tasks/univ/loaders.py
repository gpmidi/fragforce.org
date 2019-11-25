from __future__ import absolute_import, unicode_literals

import logging

from celery import shared_task
from django.conf import settings
from django.utils import timezone
from ...models import *

log = logging.getLogger("ffdonations.univ.loaders")


@shared_task(bind=True)
def load_extralife(self):
    """ Load Extra Life donations into the universal donation table """


@shared_task(bind=True)
def load_childsplay(self):
    """ Load Child's Play donations into the universal donation table """
