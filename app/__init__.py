#coding=utf-8

from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager

login_manager=LoginManager()
login_manager.session_protection="strong"
login_manager.login_view="auth.login"   #若调用所需的函数需要登录，则跳转到指定的login页面

bootstrap=Bootstrap()
mail=Mail()
db=SQLAlchemy()
#app的工厂函数
def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(config[config_name]) #加载指定的config类
    config[config_name].init_app(app)

    #初始化所有的flask扩展库
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    #注册所使用的蓝本
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_preifx="/auth")

    return app