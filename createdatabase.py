# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

basedir=os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join('data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True

db=SQLAlchemy(app)

class User(db.Model):           #用户模型
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)       #主键，由flask_sqlalchemy管理，创建后自动赋值
    email=db.Column(db.String(32),unique=True)
    username=db.Column(db.String(32))
    password=db.Column(db.String(16))
    ifpermit=db.Column(db.Boolean,default=False) #是否同意条款
    identity=db.Column(db.Integer,db.ForeignKey('identities.id'))#身份

    posts=db.relationship('Post',backref='author',lazy='dynamic')

    def __repr__(self):
        return '<User %r>'%self.username,

class Identity(db.Model):       #身份模型
    __tablename__='identities'
    id=db.Column(db.Integer,primary_key=True)
    idname=db.Column(db.String(32),unique=True)
    permissions=db.Column(db.Integer) #对应权限

    user=db.relationship('User',backref='identity',lazy='dynamic')

    def __repr__(self):
        return '<Identity %r>'%self.name

class Post(db.Model):
    __tablename__='posts'        #项目模型
    id=db.Column(db.Integer,primary_key=True)
    timestamp=db.Column(db.DateTime,index=True)
    introduction=db.Column(db.Text)
    filename=db.Column(db.Text)   #项目文件名
    author_id=db.Column(db.Integer,db.ForeignKey('users.id')) #作者

    def __repr__(self):
        return '<Pos %r>'%self.filename