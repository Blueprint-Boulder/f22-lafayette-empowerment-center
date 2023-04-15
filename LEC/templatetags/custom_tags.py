import re
from typing import Any

from django.forms import Form, BoundField
from django.forms.utils import flatatt
from django.template import Library
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe, SafeString

register = Library()

@register.simple_tag
def stylize_form(form: Form, label_classes: str, input_classes: str) -> SafeString:
    html = form.as_p()
    # I apologize for this code - Jacob
    html = re.sub(r'class\=\".*\"', '', html)
    html = re.sub(r'<label', f'<label class="{label_classes}"', html)
    html = re.sub(r'<input', f'<input class="{input_classes}"', html)
    return mark_safe(html)

@register.simple_tag
def standard_stylize_form(form: Form):
    return stylize_form(form,
                        label_classes="form-label inline-block mb-2 text-gray-700",
                        input_classes="form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none")


@register.simple_tag
def render_field(field, **kwargs):
    if field.widget_type == "select":
        field.field.widget.attrs.update(kwargs)
        placeholder = kwargs.get('placeholder', field.label)
        return render_to_string('select_with_placeholder.html',
                                {'field': field, 'placeholder': placeholder,
                                 'select_attrs': flatatt(field.field.widget.attrs | {'name': field.html_name})})
    else:
        return field.as_widget(attrs=kwargs)

#
# @register.filter
# def field_with_class(field: BoundField, html_class: str):
#     return field.as_widget(attrs={"class": html_class})
#
# @register.filter
# def field_with_placeholder(field: BoundField, placeholder: str):
#     return field.as_widget(attrs={"placeholder": placeholder})
