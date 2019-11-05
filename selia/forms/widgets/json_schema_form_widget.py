from django.forms.widgets import Widget
import json


class JsonSchemaFormWidget(Widget):
    template_name = 'selia/widgets/json_form_widget.html'
    input_type = 'text'

    def format_value(self, value):
        try:
            value = json.dumps(value)
        except TypeError:
            value = json.dumps({})
        return value
