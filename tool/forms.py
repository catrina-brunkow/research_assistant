from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, FloatField, RadioField
from wtforms.validators import  Optional, NumberRange, Regexp

class QueryForm(FlaskForm):
    WDS_name = StringField('WDS_name', validators=[Optional(), Regexp('[0-9]{5}[+,-]{1}[0-9]{4}', message='Invalid format.')])
    min_mag = FloatField('Min primary component magnitude', validators=[Optional(), NumberRange(0, 50, message='Mag invalid')])
    max_mag = FloatField('Max primary component magnitude', validators=[Optional(), NumberRange(0, 50, message='Mag invalid')])
    min_ra = IntegerField('Min RA', validators=[Optional(), NumberRange(0, 240000, message='RA invalid')])
    max_ra = IntegerField('Max RA', validators=[Optional(), NumberRange(0, 240000, message='RA invalid')])
    min_dec = IntegerField('Min DEC', validators=[Optional(), NumberRange(-900000, 900000, message='Dec invalid')])
    max_dec = IntegerField('Max DEC', validators=[Optional(), NumberRange(-900000, 900000, message='Dec invalid')])
    min_sep = FloatField('Min Separation', validators=[Optional(), NumberRange(0, 100, message='Sep invalid')])
    max_sep = FloatField('MaxSeparation', validators=[Optional(), NumberRange(0, 100, message='Sep invalid')])
    max_delta_mag = FloatField('Max Delta Mag', validators=[Optional(), NumberRange(0, 12, message='Delta Mag invalid')])
    nobs = IntegerField('Number Observations', validators=[Optional(), NumberRange(0,100, message='Number observations invalid')])
    last_obs = IntegerField('Last Observation', validators=[Optional(), NumberRange(1600, 2030, message='Last observation invalid')])
    submit = SubmitField('Search')
