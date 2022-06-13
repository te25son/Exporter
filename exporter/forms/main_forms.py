from wtforms import StringField, Form, validators  # type: ignore


class ExportForm(Form):
    annotation_id = StringField("Annotation ID", [validators.DataRequired()])
    queue_id = StringField("Queue ID", [validators.DataRequired()])

    def validate_annotation_id(self, field: StringField) -> None:
        self._check_is_valid_positive_int(field.data)

    def validate_queue_id(self, field: StringField) -> None:
        self._check_is_valid_positive_int(field.data)

    @staticmethod
    def _check_is_valid_positive_int(value: str) -> None:
        if not value.isdigit() or not int(value) >= 0:
            raise validators.ValidationError("Please use a positive integer.")
