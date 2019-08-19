from backend.forms import VueFrom
from wtforms import StringField, DateTimeField, SelectField
from wtforms.validators import DataRequired
from backend.models import Language, Committee
from backend.util import utc_to_local
from datetime import timedelta


class AddCourseForm(VueFrom):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.date.data is not None:
            self.date.data = utc_to_local(self.date.data)
        if self.duration.data is not None:
            self.duration.data = utc_to_local(self.duration.data)

    requested_by = StringField('', validators=[DataRequired("Who requested the course.")])
    date = DateTimeField('', format='%Y-%m-%dT%H:%M:%S.000Z')
    duration = DateTimeField('', format='%Y-%m-%dT%H:%M:%S.000Z')
    location = StringField('')
    language = SelectField('', choices=[(i.name, i.value) for i in Language])
    committee = SelectField('', choices=[(i.name, i.value) for i in Committee],
                            validators=[DataRequired("What committee is the course for?")])
    dances = StringField('')
    notes = StringField('')

    def model_data(self):
        return {
            "requested_by": self.requested_by.data,
            "date": self.date.data,
            "duration": timedelta(hours=self.duration.data.hour, minutes=self.duration.data.minute),
            "location": self.location.data,
            "language": self.language.data,
            "committee": self.committee.data,
            "dances": self.dances.data,
            "notes": self.notes.data,
        }
