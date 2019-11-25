# from .tasks import *
from django.conf import settings
from django.db.models import Sum
from django.utils import timezone
from memoize import memoize

from ffsfdc.models import *
from .models import *


# @memoize(timeout=120)
# def el_num_donations():
#     baseq = DonationModel.objects.filter(DonationModel.tracked_q())
#     return baseq.count()
#
#
# @memoize(timeout=120)
# def el_donation_stats():
#     baseq = DonationModel.objects.filter(DonationModel.tracked_q())
#     return baseq.aggregate(
#         sumDonations=Sum('amount'),
#         avgDonation=Avg('amount'),
#         minDonation=Min('amount'),
#         maxDonation=Max('amount'),
#     )

def event_name_maker(year=timezone.now().year):
    return 'Extra Life %d' % year


@memoize(timeout=120)
def el_teams(year=timezone.now().year):
    """ Returns a list of team IDs that we're tracking for the given year """
    from ffdonations.tasks.teams import update_teams
    yr = event_name_maker(year=year)
    ret = []
    for sa in SiteAccount.objects.filter(el_id__isnull=False).only('el_id').all():
        try:
            tm = TeamModel.objects.get(id=sa.el_id)
            if tm.event.name == yr:
                ret.append(tm.id)
        except TeamModel.DoesNotExist:
            update_teams.delay([sa.el_id, ])
    return ret


@memoize(timeout=120)
def el_contact(year=timezone.now().year):
    """ Returns a list of participant IDs that we're tracking for the given year """
    from ffdonations.tasks.participants import update_participants
    yr = event_name_maker(year=year)
    ret = []
    for sa in Contact.objects.filter(extra_life_id__isnull=False).only('extra_life_id').all():
        try:
            tm = ParticipantModel.objects.get(id=sa.extra_life_id)
            if tm.event.name == yr:
                ret.append(tm.id)
        except ParticipantModel.DoesNotExist:
            update_participants.delay([sa.extra_life_id, ])
    return ret


@memoize(timeout=120)
def el_num_donations(year=timezone.now().year):
    """ For current year """
    teams = TeamModel.objects.filter(id__in=el_teams(year=year))
    tsum = teams.aggregate(ttl=Sum('numDonations')).get('ttl', 0)
    if tsum is None:
        tsum = 0
    psum = ParticipantModel.objects.filter(id__in=el_contact(year=year), tracked=True) \
        .filter(~Q(team__in=teams)) \
        .aggregate(ttl=Sum('numDonations')).get('ttl', 0)
    if psum is None:
        psum = 0
    return dict(
        countDonations=float(tsum + psum),
        countTeamDonations=float(tsum),
        countParticipantDonations=float(psum),
    )


@memoize(timeout=120)
def el_donation_stats(year=timezone.now().year):
    """ For current year """
    teams = TeamModel.objects.filter(id__in=el_teams(year=year))
    tsum = teams.aggregate(ttl=Sum('sumDonations')).get('ttl', 0)
    if tsum is None:
        tsum = 0
    psum = ParticipantModel.objects.filter(id__in=el_contact(year=year), tracked=True) \
        .filter(~Q(team__in=teams)) \
        .aggregate(ttl=Sum('sumDonations')).get('ttl', 0)
    if psum is None:
        psum = 0
    return dict(
        sumDonations=float(tsum + psum),
        sumteamDonations=float(tsum),
        sumparticipantDonations=float(psum),
    )


@memoize(timeout=120)
def childsplay_donation_stats():
    """ For current year """
    raised = CampaignTiltifyModel.objects.filter(
        startsAt__lte=timezone.now(),
        endsAt__gte=timezone.now(),
        team__in=TeamTiltifyModel.objects.filter(slug__in=settings.TILTIFY_TEAMS)
    ).aggregate(
        total=Sum('totalAmountRaised'),
        supporting=Sum('supportingAmountRaised'),
        direct=Sum('amountRaised'),
    )
    return dict(
        totalAmountRaised=float(raised.get('total', 0) or 0),
        supportingAmountRaised=float(raised.get('supporting', 0) or 0),
        amountRaised=float(raised.get('amount', 0) or 0),
    )
