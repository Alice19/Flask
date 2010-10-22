from example import app
from example.models import EventLog

from flask import render_template, flash, url_for, redirect,session,request,current_app,request
from flask.signals import Namespace
from google.appengine.ext import db

from blinker import signal

my_signals=Namespace()
logged_in=my_signals.signal('loggedin')


@app.route('/')
def home():
    ip=request.remote_addr
    logged_in.send(current_app._get_current_object(),status="Visit happened",ip=ip)#signal generated
    return render_template('home.html')


@app.route('/login',methods=['GET','POST'])
def login():
     """check the credentials, if login happens before redirecting generate the signal"""
     logged_in.send(current_app._get_current_object(),status="Visit happened",ip=ip)#signal generated
     redirect('to the user homepage')

@logged_in.connect
def logger(sender,**kw):
    updatedstatus=kw['status']
    ip=kw['ip']
    logup=EventLog(event=updatedstatus,clientip=ip)#push the data into the table EventLog
    logup.put()







