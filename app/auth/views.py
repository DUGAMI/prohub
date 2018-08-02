#coding=utf-8

from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,login_required,logout_user,current_user
from . import auth
from ..models import User
from ..main.forms import LoginForm,RegistrationForm
from .. import db

#登录页面
@auth.route("/login",methods=["GET","POST"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        print "login"
        user=User.query.filter_by(email=form.email.data).first()
        if user!=None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get("next") or url_for("main.index"))
        flash("Invalid username or password")
    return render_template("auth/login.html",form=form)

#登出，没有页面，登出后跳转到主页
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("main.index"))

#注册页面
@auth.route("/register",methods=["GET","POST"])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        user=User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        flash("you can now login.")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html",form=form)

#每次用户对网站发出请求是调用ping函数更新最后操作时间
@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()

