from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _


def log_addition(object):
    keys = [str(x) for x in object.__dict__.keys() if not x.startswith('_')]
    values = [str(x) for x in object.__dict__.values()][1:]
    type = dict(zip(keys, values))
    l = LogEntry.objects.log_action(
        user_id=1,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.pk,
        object_repr=force_text(object),
        action_flag=ADDITION,
        change_message=_(str(type))
    )
    l.save()


def log_change(object):
    keys = [str(x) for x in object.__dict__.keys() if not x.startswith('_')]
    values = [str(x) for x in object.__dict__.values()][1:]
    type = dict(zip(keys, values))

    l = LogEntry.objects.log_action(
        user_id=1,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.pk,
        object_repr=force_text(object),
        action_flag=CHANGE,
        change_message=_(str(type))
    )
    l.save()


def log_change_mes(request, object, message):
    """
    Log that an object has been successfully changed.
    The default implementation creates an admin LogEntry object.
    """
    from django.contrib.admin.models import LogEntry, CHANGE
    if request.user.pk is None:
        user = 1
    else:
        user = request.user.pk
    l = LogEntry.objects.log_action(
        user_id=user,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.pk,
        object_repr=force_text(object),
        action_flag=CHANGE,
        change_message=message
    )
    l.save()


def log_delete(object):
    keys = [str(x) for x in object.__dict__.keys() if not x.startswith('_')]
    values = [str(x) for x in object.__dict__.values()][1:]
    type = dict(zip(keys, values))

    l = LogEntry.objects.log_action(
        user_id=1,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.pk,
        object_repr=force_text(object),
        action_flag=DELETION,
        change_message=_(str(type))
    )
    l.save()
