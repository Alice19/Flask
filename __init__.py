from flask import Flask
import settings
from werkzeug.contrib.sessions import DataBaseStore,Session
from models import MyNewSessionTable
from flask import render_template, flash, url_for, redirect,g,session,request,Flask,abort
from google.appengine.ext import db
session_store=DataBaseStore(tablename=MyNewSessionTable)
class SessionMixin(object):
    session_key='sessionid'
    def open_session(self, request):
        sid = request.cookies.get(self.session_key, None)
        if sid is None:
            return session_store.new()
        else:
            return session_store.get(sid)

    def save_session(self, session, response):
        if session.should_save:
            session_store.save(session)
            response.set_cookie(self.session_key, session.sid)
        return response

class SessionFlask(SessionMixin,Flask):
    pass

##progbegins
app=SessionFlask('travelbuddy')
app.config.from_object('travelbuddy.settings')

@app.before_request
def pull_user():
    g.user = session.get('username')
    
    

@app.route('/')
def index():
    if g.user is not None:
        return '''
        <p>You are logged in as %s.
        <p><a href=/logout>Logout</a>
        ''' %g.user
    return 'You are not logged in. <a href=/login>Login</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if username:
            session['username'] = username
            return redirect(url_for('index'))
    return '''
        <form action="" method=post>
            <p>Username:
            <input type=text name=username>
            <input type=submit value=Login>
        </form>
        '''

@app.route('/logout')
def logout():
    session['username']=None
    return redirect(url_for('index'))



