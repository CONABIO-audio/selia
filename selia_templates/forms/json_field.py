import json
from django import forms
from selia_templates.widgets.json_schema_form_widget import JsonSchemaFormWidget


class JsonField(forms.Field):
    widget = JsonSchemaFormWidget

    def __init__(self, *args, schema=None, **kwargs):
        if schema is None:
            schema = {}

        self.schema = schema

        super().__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        return {"schema": self.schema}

    def update_schema(self, schema):
        self.schema = schema
        self.widget.attrs["schema"] = self.schema

    def clean(self, value):
        if value is None:
            value = "null"

        if value == "undefined":
            value = "null"

        try:
            value = json.loads(value)
            print("VALUE", value, type(value))
            return value

        except Exception as err:
            raise forms.ValidationError(str(err))
