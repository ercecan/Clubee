from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, validators, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from user import get_user
from flask import g
from datetime import datetime
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user


class LoginForm(FlaskForm):
    username = StringField(
        'Student ID',
        validators=[
            DataRequired(),
            Length(min=9,
                   max=9,
                   message="Your Student ID Should Be 9 Characters Long")
        ],
        render_kw={'autofocus': True})
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class AdminLoginForm(FlaskForm):
    username = StringField(
        'Nickname',
        validators=[DataRequired()],
        render_kw={'autofocus': True},
    )
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In as Admin')


departments = [
    'Computer Engineering', 'Electrical Engineering', 'Mechanical Engineering',
    'Electronnics&I.E.', 'Industrial Engineering'
]


class RegistrationForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired()],
                       render_kw={'autofocus': True})
    surname = StringField('Surname', validators=[DataRequired()])
    student_id = StringField('Student ID', validators=[
        DataRequired(),
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    department = SelectField('Department',
                             choices=departments,
                             validators=[Optional()])
    gender = RadioField('Gender',
                        choices=['Female', 'Male', 'Rather Not Say'],
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',
                              validators=[DataRequired(),
                                          EqualTo('password')])
    submit = SubmitField('Register')

    ####When you add any methods that match the pattern validate_<field_name>,
    # WTForms takes those as custom validators and invokes them in addition to the stock validators.

    def validate_email(self, email):
        user = get_user(
            email=str(email.data)
        )  ##email kontrol eden query bu email varsa başka email seçtircen
        if user is not None:
            raise ValidationError('Please use a different email address.')

    def validate_student_id(self, student_id):
        user = get_user(user_id=str(student_id.data))
        if user is not None:
            raise ValidationError(
                'There already is a student with that student id.')


class UserUpdateForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired()],
                       render_kw={'autofocus': True})
    surname = StringField('Surname', validators=[DataRequired()])
    student_id = StringField('Student ID', validators=[
        DataRequired(),
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    gender = RadioField('Gender',
                        choices=['Female', 'Male', 'Rather Not Say'],
                        validators=[DataRequired()])
    submit = SubmitField('Update User')

    ####When you add any methods that match the pattern validate_<field_name>,
    # WTForms takes those as custom validators and invokes them in addition to the stock validators.

    def validate_email(self, email):
        user = get_user(email=str(email.data))
        if (user) and (email.data != current_user.email):
            raise ValidationError('This email is already in use!')

    def validate_student_id(self, student_id):
        user = get_user(user_id=str(student_id.data))
        if (user) and (student_id.data != current_user.student_id):
            raise ValidationError('This student id is already in use!')


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


class ClubUpdateForm(FlaskForm):  ##for editing and adding
    description = TextAreaField("Description", validators=[DataRequired()])
    history = TextAreaField("History", validators=[DataRequired()])
    mission = TextAreaField("Mission", validators=[DataRequired()])
    vision = TextAreaField("Vision", validators=[DataRequired()])
    # image = FileField(
    #     "Image",
    #     validators=[
    #         DataRequired(),
    #         FileAllowed(['jpg', 'png', 'jpeg'],
    #                     'Please upload .png, .jpg or .jpeg file.')
    #     ])
    source = TextAreaField("Source", validators=[DataRequired()])
    submit = SubmitField('Save Announcement')
