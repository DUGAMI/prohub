#coding=utf-8

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,ValidationError,TextAreaField,FileField
from wtforms.validators import DataRequired,Required,EqualTo,Length,Email,Regexp
from ..models import User

#表单类定义
class NameForm(FlaskForm):
    name=StringField("what is your name?",validators=[DataRequired()])
    submit=SubmitField("Submit")

#登录表单
class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(),Length(1,64),Email()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me=BooleanField("Keep me logged in")
    submit=SubmitField("Log In")

#注册表单
class RegistrationForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Length(1, 64), Email()])
    username=StringField("Username",validators=[DataRequired(),Length(1,64),Regexp("^[A-Za-z][A-Za-z0-9_.]*$",0,"Usernames must have only letters,numbers,dots or underscores")])
    password=PasswordField("Password",validators=[DataRequired(),EqualTo("password2",message="Passwords must match")])
    password2=PasswordField("Confirm password",validators=[DataRequired()])
    submit=SubmitField("Register")
    #检查邮件是否重复
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered.")
    #检查用户名是否重复
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already registered.")

#资料编辑表单
class EditProfileForm(FlaskForm):
    name=StringField("Real nmae",validators=[Length(0,64)])
    location=StringField("Location",validators=[Length(0,64)])
    about_me=TextAreaField("About me")
    submit=SubmitField("Submit")

#项目上传表单
class UploadForm(FlaskForm):
    name=StringField("Project name",validators=[Length(1,64)])
    introduction=TextAreaField("introduction")
    file=FileField("File",validators=[DataRequired()])
    submit=SubmitField("Upload")


