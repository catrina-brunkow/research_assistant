from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, FloatField, RadioField
from wtforms.validators import  Optional, NumberRange, Regexp

class QueryForm(FlaskForm):
    '''
    QueryForm class
    Used to generate a form with various fields that work as filters for searching the WDS-GAIA dataset
    Prevents users from entering invalid number ranges
    Also uses a regex to validate the wds_name field
    '''
    # Wds_name: ex: '12345+1234'
    WDS_name = StringField('WDS_name', validators=[Optional(), Regexp('[0-9]{5}[+,-]{1}[0-9]{4}', message='Invalid format.')])
    min_mag = FloatField('Min primary component magnitude', validators=[Optional(), NumberRange(0, 50, message='Mag invalid')])
    max_mag = FloatField('Max primary component magnitude', validators=[Optional(), NumberRange(0, 50, message='Mag invalid')])
    # ex: 120000 (HHMMSS)
    min_ra = IntegerField('Min RA', validators=[Optional(), NumberRange(0, 240000, message='RA invalid')])
    max_ra = IntegerField('Max RA', validators=[Optional(), NumberRange(0, 240000, message='RA invalid')])
    # ex: -75
    min_dec = IntegerField('Min DEC', validators=[Optional(), NumberRange(-90, 90, message='Dec invalid')])
    max_dec = IntegerField('Max DEC', validators=[Optional(), NumberRange(-90, 90, message='Dec invalid')])
    # ex: 8
    min_sep = FloatField('Min Separation', validators=[Optional(), NumberRange(0, 100, message='Sep invalid')])
    max_sep = FloatField('MaxSeparation', validators=[Optional(), NumberRange(0, 100, message='Sep invalid')])
    max_delta_mag = FloatField('Max Delta Mag', validators=[Optional(), NumberRange(0, 12, message='Delta Mag invalid')])
    nobs = IntegerField('Number Observations', validators=[Optional(), NumberRange(0,100, message='Number observations invalid')])
    last_obs = IntegerField('Last Observation', validators=[Optional(), NumberRange(1600, 2030, message='Last observation invalid')])
    submit = SubmitField('Search')
