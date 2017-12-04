from flask import Flask, render_template, flash, redirect
from MiniBank.Config import config
from .forms import CreateUserForm

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


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', user=config.admin_name)

@app.route('/events')
def events():
    events = application_service.event_repository.get_all_events('last') 
    events = map(dict, events)
    events = map(lambda evt: json.dumps(evt, indent=4), events)
    return render_template('events.html', events=events)

@app.route('/create_user', methods=["GET", "POST"])
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        flash('User creation requested for UserName="%s", IsPerson=%s' % (form.username.data, str(form.is_person.data)))

        user_service.create_user(form.username.data, form.is_person.data)

        return redirect('/index')
    return render_template('create_user.html', form=form)

@app.route('/users', methods=["GET"])
def get_users():
    return render_template('users.html')

















def run(application_service_arg, account_service_arg, user_service_arg, debug=False):
    global application_service, account_service, user_service
    application_service = application_service_arg
    account_service = account_service_arg
    user_service = user_service_arg

    app.run(debug=debug)
