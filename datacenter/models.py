from django.db import models
from django.utils.timezone import localtime


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )

def get_duration(visit):
    entrance_time = localtime(visit.entered_at)
    local_time = localtime()
    delta = local_time - entrance_time
    duration = delta.total_seconds()
    return duration


def format_duration(duration):
    formatted_duration = f'{int(duration) // 3600}:{(int(duration) % 3600) // 60}'
    return formatted_duration


def is_visit_long(visit, minutes=60):
    if visit.leaved_at is not True:
        entrance_time = localtime(visit.entered_at)
        leaving_time = localtime(visit.leaved_at)
        delta = leaving_time - entrance_time
        visit_duration = delta.seconds
        visit_duration = visit_duration / 60
        if visit_duration > minutes:
            return True
        else:
            return False
    else:
        visit_duration = get_duration(visit)
        visit_duration = visit_duration / 60
        if visit_duration > minutes:
            return True
        else:
            return False