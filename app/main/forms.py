from wtforms import (
    Form, 
    StringField, 
    TextAreaField, 
    PasswordField, 
    BooleanField, 
    SubmitField, 
    FileField,
    validators, 
    ValidationError,
    )
from ..models import (
    User, 
    Post, 
    Question, 
    Answer,
    )
from flask_pagedown.fields import PageDownField


class PostForm(Form):
    title = StringField('题目', validators=[validators.Length(min=1, max=64)])
    body = PageDownField('写下你的内容', validators=[validators.DataRequired()])


class QuestionForm(Form):
    title = StringField('问题题目', validators=[validators.Length(min=1, max=64)])
    body = PageDownField('问题描述')


class AnswerForm(Form):
    body = PageDownField('回答内容', validators=[validators.DataRequired()])


class EditProfileForm(Form):
    name = StringField('姓名', validators=[validators.Length(0, 64)])
    location = StringField('地址', validators=[validators.Length(0, 64)])
    about_me = TextAreaField('关于我')