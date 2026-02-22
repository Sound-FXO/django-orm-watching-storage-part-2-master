from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import localtime
from datacenter.models import get_duration, format_duration
from datacenter.models import is_visit_long


def storage_information_view(request):
    still_inside = Visit.objects.filter(leaved_at=None)

    non_closed_visits = []

    for person in still_inside:
        duration = format_duration(get_duration(person))
        person_name = person.passcard
        entrance_time = localtime(person.entered_at)
        is_strange = is_visit_long(person)
        person_data = {
                "who_entered": person_name,
                "entered_at": entrance_time,
                "duration": duration,
                "is_strange": is_strange,
        }
        non_closed_visits.append(person_data)

    context = {
        "non_closed_visits": non_closed_visits,
    }
    return render(request, "storage_information.html", context)
