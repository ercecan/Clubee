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
    """
    login form using flask form
    """
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
    """
    login form for admins using flask form
    """
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
    """
    registration form for normal users
    """
    name = StringField('Name',
                       validators=[DataRequired()],
                       render_kw={'autofocus': True})
    surname = StringField('Surname', validators=[DataRequired()])
    student_id = StringField(
        'Student ID',
        validators=[
            DataRequired(),
            Length(min=9,
                   max=9,
                   message="Your Student ID Should Be 9 Characters Long")
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
        """
        checks if the same email is already registered to the database
        if it is then raises validation error
        """
        user = get_user(
            email=str(email.data)
        )  ##email kontrol eden query bu email varsa başka email seçtircen
        if user is not None:
            raise ValidationError('Please use a different email address.')

    def validate_student_id(self, student_id):
        """
        checks if the same student id is already registered to the database
        if it is then raises validation error
        """
        user = get_user(user_id=str(student_id.data))
        if user is not None:
            raise ValidationError(
                'There already is a student with that student id.')


class UserUpdateForm(FlaskForm):
    """
    a form for users to update their account info
    """
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
        """
        checks if the same email is already registered to the database
        if it is then raises validation error
        """
        user = get_user(email=str(email.data))
        if (user) and (email.data != current_user.email):
            raise ValidationError('This email is already in use!')

    def validate_student_id(self, student_id):
        """
        checks if the same student id is already registered to the database
        if it is then raises validation error
        """
        user = get_user(user_id=str(student_id.data))
        if (user) and (student_id.data != current_user.student_id):
            raise ValidationError('This student id is already in use!')


class CommentForm(FlaskForm):
    """
    form for posting comments
    """
    content = TextAreaField(
        'Comment', validators=[Length(min=0, max=140),
                               DataRequired()])
    submit = SubmitField('Post comment')


class AnnouncementForm(FlaskForm):  ##for editing and adding
    """
    form used by admins to add or edit announcements
    """
    header = TextAreaField("Header", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    image = FileField(
        "Image",
        validators=[
            Optional(),
            FileAllowed(['jpg', 'png', 'jpeg'],
                        'Please upload .png, .jpg or .jpeg file.')
        ])
    submit = SubmitField('Save Announcement')


class EventForm(FlaskForm):  ##for editing and adding
    """
    form used by admins to add or edit events
    """
    header = TextAreaField("Header", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    image = FileField(
        "Image",
        validators=[
            Optional(),
            FileAllowed(['jpg', 'png', 'jpeg'],
                        'Please upload .png, .jpg or .jpeg file.')
        ])
    date = DateField("Event Date",
                     format='%Y-%m-%d',
                     validators=[DataRequired()])  #optional or required?
    submit = SubmitField('Save Event')


class ClubUpdateForm(FlaskForm):  ##for editing
    """
    form used by admins to edit club info
    """
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
