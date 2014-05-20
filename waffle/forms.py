import json

from django import forms

from waffle.models import Flag
from waffle.customsegment import get_custom_segment_form



class FlagForm(forms.ModelForm):
    class Meta:
        model = Flag

    def clean_custom_segment(self):
        custom_segment = self.cleaned_data.get('custom_segment')
        if not custom_segment:
            return custom_segment

        CustomSegmentForm = get_custom_segment_form()
        if CustomSegmentForm is None:
            raise forms.ValidationError(
                'WAFFLE_CUSTOM_SEGMENT form is not defined and this field '
                'should be empty.'
            )

        try:
            data = json.loads(custom_segment)
        except ValueError as e:
            raise forms.ValidationError('Error while parsing JSON: %s' % e)

        form = CustomSegmentForm(data)
        if not form.is_valid():
            raise forms.ValidationError(form.errors.as_ul())

        # Check if provided data have extra fields.
        userkeys = set(data.keys())
        formkeys = set(form.cleaned_data.keys())
        diff = userkeys.difference(formkeys)
        if diff:
            raise forms.ValidationError(
                'Unknown fields: %s' % ','.join(diff)
            )

        return custom_segment
