from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Optional


class SubmitSearchForm(FlaskForm):
    key = SelectField('Select Type', choices=[('bid', 'Bill ID'),
                                              ('bs', 'Bill Sponsor'),
                                              ('txt', 'Bill Text')])
    repo_url = StringField('Search')
    keywords = SelectField('Keywords', choices=[('none', 'Select Keyword'),
                                                ('op', 'Operations'),
                                              ('gg', 'General Government'),
                                              ('ed', 'Education'),
                                                ('fi', 'Finance'),
                                                ('hl', 'Health'),
                                                ('tr', 'Transportation'),
                                                ('ag', 'Agriculture'),
                                                ('en', 'Environment')
                                                ])
    submit = SubmitField('GO')
