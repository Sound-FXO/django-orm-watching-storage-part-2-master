from datacenter.models import Passcard
from datacenter.models import Visit
from datacenter.models import format_duration
from datacenter.models import is_visit_long
from django.utils.timezone import localtime
from django.shortcuts import render
from django.shortcuts import get_object_or_404


def passcard_info_view(request, passcode):

    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []

    for visit in visits:
        entered_at = visit.entered_at
        delta = localtime(visit.leaved_at) - localtime(visit.entered_at)
        duration = format_duration(delta.total_seconds())
        is_strange = is_visit_long(visit)
        visit_data = {
            "entered_at": entered_at,
            "duration": duration,
            "is_strange": is_strange
        }
        this_passcard_visits.append(visit_data)

    context = {"passcard": passcard, "this_passcard_visits": this_passcard_visits}
    return render(request, "passcard_info.html", context)
