from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, validators, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from user import get_user
from flask import g
from datetime import datetime
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField


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
    submit = SubmitField('Update User')

    ####When you add any methods that match the pattern validate_<field_name>,
    # WTForms takes those as custom validators and invokes them in addition to the stock validators.


def validate_mail(connection, email):
    try:
        with connection.cursor() as cursor:
            if email:
                q = """select * from users where email = %(email)s"""
                data = {'email': str(email)}
                cursor.execute(q, data)
                user = cursor.fetchone()
                if user:
                    return user
                return None
    except Exception as e:
        print("error while validating mail", e)


def validate_studentid(connection, student_id):
    try:
        user = get_user(user_id=str(student_id))
        if user is not None:
            return True
    except Exception as e:
        print("error while validating studentid", e)


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
