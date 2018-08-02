#coding=utf-8
from flask import render_template,session,redirect,url_for

from . import main
from flask import abort,flash,make_response,send_file
from flask_login import login_required,current_user
from .forms import NameForm,LoginForm,EditProfileForm,UploadForm
from ..models import User,Project
from ..import db

import os
import hashlib


@main.route('/',methods=["GET","POST"])
def index():
    l=Project.query.all()
    return render_template("index.html",Project=l)


#用户页面
@main.route("/user/<username>",methods=["GET","POST"])
def user(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template("user.html",user=user)

#项目界面
@main.route("/project/<proname>",methods=["GET","POST"])
def project(proname):
    project=Project.query.filter_by(name=proname).first()
    if project is None:
        abort(404)
    return render_template("project.html",project=project)

#资料编辑页面
@main.route("/edit-profile",methods=["GET","POST"])
@login_required
def edit_profile():
    form=EditProfileForm()
    if form.validate_on_submit():
        current_user.name=form.name.data
        current_user.location=form.location.data
        current_user.about_me=form.about_me.data
        db.session.add(current_user)
        flash("Your profile has been updated")
        return redirect(url_for(".user",username=current_user.username))

    #加载已有的资料 current_user本质上是user对象，貌似是models模块中调用的load_user函数加载的信息
    form.name.data=current_user.name
    form.location.data=current_user.location
    form.about_me.data=current_user.about_me
    return render_template("edit-profile.html",form=form)

@main.route("/upload",methods=["GET","POST"])
@login_required
def upload():
    form=UploadForm()
    # 将文件上传到upload文件夹，文件命名方式使用用户的邮箱经过散列函数加密然后再加上文件名的方式命名
    if form.validate_on_submit():
        file = form.file.data
        emailMd5 = hashlib.md5(current_user.email).hexdigest()
        basedir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        dir = basedir + "/upload/" + emailMd5 + "-" + file.filename
        file.save(dir)
        print dir
        flash("File Upload Success!")

        p=Project(name=form.name.data,filePath=dir,user_id=current_user.id,introduction=form.introduction.data)
        db.session.add(p)

        return redirect(url_for(".user", username=current_user.username))

    return render_template("upload.html",form=form)

@main.route("/download/<filename>")
def download(filename):

    pro=Project.query.filter_by(id=filename).first()
    response=make_response(send_file(pro.filePath,as_attachment=True))
    return response