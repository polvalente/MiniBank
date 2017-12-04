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
        flash('Account creation requested for uid="%d", initial_balance=$%.02f' % (form.owner_id.data, form.initial_balance.data))

        user_service.create_account(int(form.owner_id.data), float(form.initial_balance.data))

        return redirect('/users')
    return render_template('create_account.html', form=form)

@app.route('/deposit_account', methods=["GET", "POST"])
def deposit_account():
    form = DepositForm()
    if form.validate_on_submit():
        flash('Deposit to account requested for account id="%d" with value "$%.02f"' % (form.account_id.data, form.transaction_value.data))

        account_service.deposit_to_account(int(form.account_id.data), float(form.transaction_value.data))
        return redirect('/users')
    return render_template('transaction.html',transaction_type="Deposit", form=form)

@app.route('/withdraw_account', methods=["GET", "POST"])
def withdraw_account():
    form = WithdrawForm()
    if form.validate_on_submit():
        flash('Withdraw from account requested for account id="%d" with value "$%.02f" by user id="%d"' % (form.account_id.data, form.transaction_value.data, form.user_id.data))

        account_service.withdraw_from_account(int(form.user_id.data), int(form.account_id.data), float(form.transaction_value.data))
        return redirect('/users')
    return render_template('transaction.html', transaction_type="Withdraw", form=form)

@app.route('/account_summary', methods=["GET", "POST"])
def get_account_summary():
    form = AccountSummaryForm()
    if form.validate_on_submit():
        summary = user_service.get_account_summary(int(form.user_id.data))
        return render_template('account_summary.html', account_summary=summary, form=form)
    return render_template('account_summary.html', form=form)










def run(application_service_arg, account_service_arg, user_service_arg, debug=False):
    global application_service, account_service, user_service
    application_service = application_service_arg
    account_service = account_service_arg
    user_service = user_service_arg

    app.run(debug=debug)
