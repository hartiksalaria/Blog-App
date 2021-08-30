from wtforms import Form, StringField, SubmitField, TextField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo


class RegisterForm(Form):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = StringField('password', validators=[DataRequired()])
    confirm_password = StringField('confirm password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    remember_me = BooleanField('remember')
    submit = SubmitField('submit')


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember')
    submit = SubmitField('submit')


class PostForm(Form):
    content = TextField('post', validators=[DataRequired()])
    title = TextField('title', validators=[DataRequired()])
    submit = SubmitField('submit')


class CommentForm(Form):
    content = TextField('comment', validators=[DataRequired()])
    submit = SubmitField('submit')
    

class UserEditForm(Form):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    previous_password = StringField('previous_password', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    confirm_password = StringField('confirm_password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('submit')