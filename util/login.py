# coding: utf-8

"""
管理用户

Usage:
--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--
from flask import Flask, request, redirect
import login

app = Flask(__name__)
login.init(app, 'sign_in')

@app.route('/')
@login.login_required
def index():
    return 'Index!'

def sign_up():
    pass

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'GET':
        return '''
               <form action='sign_in' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''
    if request.form['email'] == '123':
        login.login('123')
        return redirect('/')
    return 'login error!'

@app.route('/sign_out')
def sign_out():
    login.logout()
    return redirect('/')
--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--
"""

import flask_login
from flask_login import login_required

login_manager = flask_login.LoginManager()


class User(flask_login.UserMixin):
    def __init__(self, user_id):
        self.id = user_id


def init(app, login_view=None):
    """
    :param app: from Flask(xxx)
    :param login_view: login_manager.login_view 用来显示登陆界面的函数
    :return: None
    """
    login_manager.init_app(app)
    login_manager.login_view = login_view


@login_manager.user_loader
def load_user(_id):
    return User(_id)


def login(user_id):
    user = User(user_id)
    flask_login.login_user(user)


@login_required
def logout():
    flask_login.logout_user()


def get_cur_user_id():
    return flask_login.current_user.id
