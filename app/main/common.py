#coding=utf-8
from wtforms.validators import required,EqualTo,DataRequired
from wtforms import StringField,SubmitField,PasswordField
from flask_wtf import FlaskForm
from threading import Thread
import os

basedir=os.path.dirname(__file__)


#异步模式发送邮件
def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

def send_email(to,subject,template,**kwargs):
    msg=Message(app.config["FLASKY_MAIL_SUBJECT_PREFIX"]+subject,sender="gami000@163.com",recipients=[to])
    msg.body=render_template(template+".txt",**kwargs)
    msg.html=render_template(template+".html",**kwargs)
    #创建新线程
    thr=Thread(target=send_async_email,args=[app,msg])
    thr.start()
    return thr

if(__name__=="__main__"):
    app.run(debug=True)

