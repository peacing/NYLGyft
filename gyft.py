from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import Required
import csv
import json
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string6'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

class CityPick(Form):
    city = SelectField('Pick a city:', choices=[('NYC', 'New York City'),('BRK', 'Berkely'),
    ('BOS', 'Boston'),('BAL', 'Baltimore'),('HBK', 'Hoboken'),('PHL', 'Philadelphia'),
    ('AST', 'Austin'),('MIA', 'Miami'),('CHI', 'Chicago')])
    submit = SubmitField('Submit')

class NameForm(Form):
    name = StringField('Client Name:', validators=[Required()])
    address = StringField('Dropoff Address:', validators=[Required()])
    gift = SelectField('Gift:', choices=[('Wine', 'Wine Bottle'),('Diapers', 'Diapers'),('Crystal Stemware', 'Crystal Stemware')])
    pmessage = StringField('Personalized Message:', validators=[Required()])
    submit = SubmitField('Submit')
    
class LoginForm(Form):
    username = StringField('Username:')
    password = PasswordField('Password:')
    login = SubmitField('Log In!')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/')
def index():
    return render_template('index.html', username=session.get('username'))

@app.route('/cities', methods=['GET', 'POST'])
def cities():
    city = None
    form = CityPick()
    if form.validate_on_submit():
        city = form.city.data
        form.city.data= ''
        return redirect('/submit')
    return render_template('cities.html', form=form, city=city)

    
#@app.route('/user/<name>')
#def user(name):
#    return render_template('user.html', name=name)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    address = None
    gift = None
    pmessage = None
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        address = form.address.data
        session['dropoff_address'] = form.address.data
        gift = form.gift.data
        session['gift'] = form.gift.data
        pmessage = form.pmessage.data
        #if old_name is not None and old_name != form.name.data:
            #flash('Looks like you have changed your name!')
        form.name.data = ''
        form.address.data = ''
        form.gift.data = ''
        form.pmessage.data = ''
        return redirect('/postmates_delivery')
    return render_template('submit.html', form=form, name=name, address=address, gift=gift, pmessage=pmessage)
    
@app.route('/postmates_delivery')
def postmates_delivery():

    # Preparing API call
    PM_Test_APIKey = 'd184ecab-5f46-42fd-bbfc-28b73b88cf4e'
    PM_cust_id = 'cus_KAay_YCGWhyi_k'
    url = 'https://api.postmates.com'
    url_delivery = url + '/v1/customers/' + PM_cust_id + '/delivery_quotes'
    headers = {'user': 'd184ecab-5f46-42fd-bbfc-28b73b88cf4e'}
    dropoff_address = session.get('dropoff_address')
    data = {'pickup_address': '51 Madison Avenue New York City, NY 10010',
    'dropoff_address': dropoff_address}
    
    # Sending API request
    resp = requests.post(url_delivery, data=data, auth=HTTPBasicAuth('d184ecab-5f46-42fd-bbfc-28b73b88cf4e', ''))

    # Parsing API response
    rj = resp.json()
    c_vals = (rj['created'].lstrip('0123456789-').lstrip('T').rstrip('Z')).split(':')
    eta_vals = (rj['dropoff_eta'].lstrip('0123456789-').lstrip('T').rstrip('Z')).split(':')
    fee = ('$'+str(int(rj['fee'])/100.0)+'0')[:6]

    # Return fee, request time, and expected delivery time (eta)
    #return str(json.dumps({'fee': fee, 'created':str(int(c_vals[0]) - 5) +':'+ c_vals[1] +':'+ c_vals[2], 'eta': str(int(eta_vals[0]) - 5) +':'+ eta_vals[1] +':'+ eta_vals[2]}))
    return render_template('postmates_delivery.html', eta=eta_vals, fee=fee, drop_address=session.get('dropoff_address'), item=session.get('gift'))
    
@app.route('/congrats')
def congrats():
    return render_template('congrats.html')
    
@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    username = None
    password = None
    form = LoginForm()
    if form.validate_on_submit():
        session['username'] = form.username.data
        password = form.password.data
        form.username.data = ''
        form.password.data = ''
        return redirect('/')
    return render_template('log_in.html', form=form, username=session.get('username'), password=password)
    


if __name__ == '__main__':
    manager.run()
