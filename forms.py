from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from user import get_user
from flask import g
from datetime import datetime
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField


class LoginForm(FlaskForm):
    username = StringField('Student ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class AdminLoginForm(FlaskForm):
    username = StringField('Nickname', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In as Admin')


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    student_id = StringField('Student ID', validators=[
        DataRequired(),
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    department = StringField('Department', validators=[Optional()])
    """
    department = SelectField(u'Your Department in ITU',
                             choices=[
                                 ('ce', 'Computer Engineering'),
                                 ('ai', 'AI and Data Science Engineering'),
                                 ('ece',
                                  'Electronics and Communication Engineering'),
                                 ('ee', 'Electrical Engineering')
                             ])
    """
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',
                              validators=[DataRequired(),
                                          EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, student_id):
        user = get_user(user_id=studestudent_id)
        if user is not None:
            raise ValidationError('Please use a different username.')

    """
    def validate_email(self, email):
        user = get_user(email=email)##email kontrol eden query bu email varsa başka email seçtircen
        if user is not None:
            raise ValidationError('Please use a different email address.')
    """


class CommentForm(FlaskForm):
    content = TextAreaField(
        'Comment', validators=[Length(min=0, max=140),
                               DataRequired()])
    submit = SubmitField('Post comment')


class AnnouncementForm(FlaskForm):  ##for editing and adding
    header = TextAreaField("Header", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    image = FileField("Image", validators=[Optional()])
    submit = SubmitField('Save Announcement')


class EventForm(FlaskForm):  ##for editing and adding
    header = TextAreaField("Header", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    image = FileField("Image", validators=[Optional()])
    date = DateField("Event Date", format='%Y-%m-%d')  #optional or required?
    submit = SubmitField('Save Event')
