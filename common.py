#coding=utf-8

from flask import Flask,render_template,session,redirect,url_for,flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.validators import required,EqualTo
from wtforms import StringField,SubmitField,PasswordField
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail,Message
from threading import Thread
import os

basedir=os.path.dirname(__file__)

app=Flask(__name__)


app.config["SECRET_KEY"]="hard to guess string"

#数据库配置
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///"+os.path.join(basedir,"data.sqlite")
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"]=True

#邮件配置
app.config["MAIL_SERVER"]="smtp.163.com"
app.config["MAIL_PORT"]=465
app.config["MAIL_USE_SSL"]=True
app.config["MAIL_USERNAME"]=""
app.config["MAIL_PASSWORD"]=""
app.config["FLASKY_MAIL_SUBJECT_PREFIX"]="[Flasky]"

bootstrap=Bootstrap(app)
db=SQLAlchemy(app)
mail=Mail(app)

#定义数据库的数据模型
class User(db.Model):
    __tablename__ = "users"
    email = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(64), primary_key=True)

    def __repr__(self):
        return "<User {} {}>".format(self.email,self.password)

#表单类定义
class NameForm(FlaskForm):
    name=StringField("what is your name?",validators=[required()])
    submit=SubmitField("Submit")

class registerForm(FlaskForm):
    email=StringField(validators=[required()])
    #validators有多个验证函数代表要进行多层验证
    password=PasswordField("password",validators=[required(),EqualTo("confirm",message="Passwords must match")])
    confirm=PasswordField("Repeat Password")
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    email = StringField(validators=[required()])
    password = PasswordField("password", validators=[required()])
    submit=SubmitField("submit")

#异步模式发送邮件
def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

def send_email(to,subject,template,**kwargs):
    msg=Message(app.config["FLASKY_MAIL_SUBJECT_PREFIX"]+subject,sender="",recipients=[to])
    msg.body=render_template(template+".txt",**kwargs)
    msg.html=render_template(template+".html",**kwargs)
    #创建新线程
    thr=Thread(target=send_async_email,args=[app,msg])
    thr.start()
    return thr

@app.route('/',methods=["GET","POST"])
def index():
    form=NameForm()

    if form.validate_on_submit():
        user=User.query.filter_by(username=form.name.data).first()
        #如果是新用户就发一封邮件
        if user is None:
            user=User(username=form.name.data)
            db.session.add(user)
            session["known"]=False
            send_email("","New User","mail/new_user",user=user)
        else:
            session["known"]=True
        session["name"]=form.name.data
        form.name.data=""
        return redirect(url_for("index"))
    return render_template("index.html",form=form,name=session.get("name"),known=session.get("known"))

@app.route("/user/<name>")
def user(name):
    return render_template("user.html",name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"),500

@app.route("/home",methods=["GET","POST"])
def home():
    form=registerForm()

    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first() is None:
            user=User(email=form.email.data,password=form.password.data)
            db.session.add(user)
            return redirect(url_for("index"))

    return render_template("home.html", form=form)

@app.route("/login",methods=["GET","POST"])
def login():
    form=LoginForm()

    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user.password==form.password.data:
            return redirect("Success.html")
        else:
            print "wrong"
    return render_template("login.html",form=form)

if(__name__=="__main__"):
    app.run(debug=True)