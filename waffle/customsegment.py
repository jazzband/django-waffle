import json

from django.conf import settings
from django.utils.module_loading import import_by_path


def get_custom_segment_form(custom_segment_form=None):
    if custom_segment_form is None:
        custom_segment_form = getattr(settings, 'WAFFLE_CUSTOM_SEGMENT', None)

    if custom_segment_form is not None:
        CustomSegmentForm = import_by_path(custom_segment_form)
        return CustomSegmentForm


def check_custom_segment(flag, request):
    if not flag.custom_segment:
        return False

    CustomSegmentForm = get_custom_segment_form()
    if CustomSegmentForm is None:
        return False

    try:
        data = json.loads(flag.custom_segment)
    except ValueError:
        return False

    form = CustomSegmentForm(data)
    return form.flag_is_active(flag, request, data)
