from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, RadioField, HiddenField
from wtforms.validators import DataRequired

class PageSelect(FlaskForm):
    page = SelectField('Title', [DataRequired()])

class NavPanel(FlaskForm):

    first_doc_id = HiddenField()
    last_doc_id = HiddenField()
    page = HiddenField()

    active_check = BooleanField()
    sold_check = BooleanField()

    date_selection = RadioField(
        default = 'Last 3 days',
        choices = [
            'Last 1 day', 'Last 3 days',
            'Last 7 days','All time'
        ]
    )

    maxamount = IntegerField()
    minamount = IntegerField()
    submit = SubmitField('Apply filters')

    next_submit = SubmitField('Next')

    prev_submit = SubmitField('Prev')



    