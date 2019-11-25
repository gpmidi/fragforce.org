from __future__ import absolute_import, unicode_literals

import logging

from celery import shared_task
from django.conf import settings
from django.utils import timezone
from ...models import *

baseLog = logging.getLogger("ffdonations.univ.loaders")


@shared_task(bind=True)
def load_extralife(self):
    """ Load Extra Life donations into the universal donation table """
    log = baseLog.getChild("extralife")
    for missing in DonationModel.objects.filter(univ=None).filter(DonationModel.tracked_q()).all()[:10000]:
        ndonation = Donation(
            charity=Donation.CHARITY_EL,
            donated_at=missing.created,
            donation_amount=missing.amount,
            currencyisocode=Donation.CURR_USD,
        )
        ndonation.save()
        missing.univ = ndonation.pk
        missing.save()


@shared_task(bind=True)
def load_childsplay(self):
    """ Load Child's Play donations into the universal donation table """
    pass
