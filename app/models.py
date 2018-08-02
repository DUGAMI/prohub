#coding=utf-8
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask import current_app,request
from flask_login import UserMixin,AnonymousUserMixin
from . import login_manager
from datetime import datetime
import hashlib

#在调用user_login函数后Flask—login会调用这个函数加载用户信息
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 定义数据库的数据模型
class User(UserMixin,db.Model):
    __tablename__ = "users"
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64))
    location=db.Column(db.String(64))
    about_me=db.Column(db.Text())
    member_since=db.Column(db.DateTime(),default=datetime.utcnow)    #用户注册时间
    last_seen=db.Column(db.DateTime,default=datetime.utcnow)        #用户最后一次活动的时间
    email=db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64), unique=True,index=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))  #为用户指定权限
    projects=db.relationship("Project",backref="user", lazy="dynamic")

    password_hash=db.Column(db.String(128)) #进过散列函数加密的密码

    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        #如果邮箱为系统指定的邮箱，那么权限就是管理员等级，否则为普通用户
        if self.role is None:
            if self.email==current_app.config["FLASKY_ADMIN"]:
                self.role=Role.query.filter_by(permissions=0xFF).first()
            if self.role is None:
                self.role=Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise ArithmeticError("password is not a readable attribute")

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    #将密码使用散列函数处理，并且设为只写模式
    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)

    #检测用户是否能进行permissions所指定的权限或者是否具有相应的权限
    def can(self,permissions):
        return self.role!=None and (self.role.permissions&permissions)==permissions

    #检测用户是否具有管理员权限
    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    #每一次进行访问操作时更新最后访问时间
    def ping(self):
        self.last_seen=datetime.utcnow()
        db.session.add(self)

    def gravatar(self,size=100,default="identicon",rating="g"):
        if request.is_secure:
            url="https://secure.gravatar.com/avatar"
        else:
            url="http://www.gravatar.com/avatar"
        hash=hashlib.md5(self.email.encode("utf-8")).hexdigest()
        return "{url}/{hash}?s={size}&d={default}&r={rating}".format(url=url,hash=hash,size=size,default=default,rating=rating)

    def __repr__(self):
        return "<User {}>".format(self.username)

#未登录用户
class AnonymousUser(AnonymousUserMixin):
    def can(self,permissinos):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user=AnonymousUser

#操作权限设置
class Permission:
    FOLLOW=0X01
    COMMENT=0X02
    WRITE_ARTICLES=0X04
    MODERATE_COMMENTS=0X08
    ADMINISTER=0X80


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default=db.Column(db.Boolean,default=False,index=True)
    permissions=db.column(db.Integer)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return "<Role {}>".format(self.name)

    #权限设置脚本方法，通过对操作权限进行按位与运算组合出相应的权限角色，其中管理员的值最大，表示可以进行任意的操作
    @staticmethod
    def insert_roles():
        roles={
            "User":(Permission.FOLLOW|Permission.COMMENT|Permission.WRITE_ARTICLES,True),
            "Moderator":(Permission.FOLLOW|Permission.COMMENT|Permission.WRITE_ARTICLES|Permission.MODERATE_COMMENTS,False),
            "Administrator":(0xFF,False)
        }
        for r in roles:
            role=Role.query.filter_by(name=r).first()
            if role==None:
                role=Role(name=r)
            role.permissions=roles[r][0]
            role.default=roles[r][1]
            db.session.add(role)
        db.session.commit()

class Project(db.Model):
    __tablename__="projects"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64))
    filePath=db.Column(db.String(64))
    #每个project都有一个用户外键，可以为一个项目指定一个用户，一个用户可以建立多个项目，是一对多的关系
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"))

    introduction=db.Column(db.Text())

    def __repr__(self):
        return "<Project {}>".format(self.name)