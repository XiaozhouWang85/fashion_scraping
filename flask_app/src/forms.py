from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, RadioField
from wtforms.validators import DataRequired

class PageSelect(FlaskForm):
    page = SelectField('Title', [DataRequired()])

class NavPanel(FlaskForm):
    active_check = BooleanField()
    sold_check = BooleanField()

    date_selection = RadioField(
        default = 'All time',
        choices = [
            'Last 1 day', 'Last 3 days',
            'Last 7 days','All time'
        ]
    )

    maxamount = IntegerField(default=60)
    minamount = IntegerField(default=40)
    submit = SubmitField('Apply filters')



    