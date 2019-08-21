from backend.forms import VueFrom
from wtforms import StringField, DateTimeField, SelectField
from wtforms.validators import DataRequired
from backend.models import Language, Committee
from datetime import timedelta
from backend.values import DATETIME_FORMAT


class AddCourseForm(VueFrom):

    requested_by = StringField('', validators=[DataRequired("Who requested the course.")])
    date = DateTimeField('', format=DATETIME_FORMAT)
    duration = DateTimeField('', format=DATETIME_FORMAT)
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
