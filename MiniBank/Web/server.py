from flask import Flask, render_template, flash, redirect
from MiniBank.Config import config
from .forms import *

import json
     

app = Flask(__name__)
app.config.update(
        DEBUG=True,
        WTF_CSRF_ENABLE = True,
        SECRET_KEY = "my-key-is-so-secret-it-hurts"
        ) 


application_service = None
account_service = None
user_service = None


def pretty_json(data):
    return json.dumps(data, sort_keys=True, indent = 2, separators=(',', ': '))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', user=config.admin_name)

@app.route('/events')
def events():
    events = application_service.event_repository.get_all_events('last') 
    events = map(dict, events)
    events = map(pretty_json, events)
    return render_template('events.html', events=events)

@app.route('/create_user', methods=["GET", "POST"])
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        flash('User creation requested for UserName="%s", IsPerson=%s' % (form.username.data, str(form.is_person.data)))

        user_service.create_user(form.username.data, form.is_person.data)

        return redirect('/users')
    return render_template('create_user.html', form=form)

@app.route('/users', methods=["GET"])
def get_users():
    users = application_service.application_state.users.values()
    users = map(dict, users)
    users = map(pretty_json, users)
    return render_template('users.html', users=users)

@app.route('/accounts', methods=["GET"])
def get_accounts():
    accounts = application_service.application_state.accounts.values()
    accounts = map(dict, accounts)
    accounts = map(pretty_json, accounts)
    return render_template('accounts.html', accounts=accounts)

@app.route('/create_account', methods=["GET", "POST"])
def create_account():
    form = CreateAccountForm()
    if form.validate_on_submit():
        flash('Account creation requested for uid="%d", initial_balanca=%.02f' % (form.owner_id.data, form.initial_balance.data))

        user_service.create_account(form.owner_id.data, float(form.initial_balance.data))

        return redirect('/accounts')
    return render_template('create_account.html', form=form)







def run(application_service_arg, account_service_arg, user_service_arg, debug=False):
    global application_service, account_service, user_service
    application_service = application_service_arg
    account_service = account_service_arg
    user_service = user_service_arg

    app.run(debug=debug)
