#coding=utf-8

import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY=os.environ.get("SECRET_KEY") or "hard to guess string"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    FLASKY_MAIL_SUBJECT_PREFIX = "[Flasky]"
    FLASKY_MAIL_SENDER="Flasky Admin<gami000@163.com>"
    FLASKY_ADMIN=os.environ.get("FLASKY_ADMIN")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG=True

    # 邮件配置
    MAIL_SERVER = "smtp.163.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = "gami000"
    MAIL_PASSWORD = "s12345678"
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data.sqlite")

class TestingConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI=os.environ.get("EST_DATABASE_URL") or  "sqlite:///" + os.path.join(basedir, "data-test.sqlite")

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL") or  "sqlite:///" + os.path.join(basedir, "data.sqlite")

config={
    "development":DevelopmentConfig,
    "testing":TestingConfig,
    "production":ProductionConfig,
    "default":DevelopmentConfig
}