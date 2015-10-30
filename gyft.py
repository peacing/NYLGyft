from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

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
    address = StringField('Address:', validators=[Required()])
    gift = SelectField('Gift:', choices=[('Wine', 'Wine Bottle'),('Baby', 'Diapers'),('Dog', 'Invisible Dog Fence')])
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
    return render_template('index.html')

@app.route('/cities', methods=['GET', 'POST'])
def cities():
    city = None
    form = CityPick()
    if form.validate_on_submit():
        city = form.city.data
        form.city.data= ''
        return redirect('/submit')
    return render_template('cities.html', form=form, city=city)

#@app.route('/', methods=['GET', 'POST'])
#def index():
#    address = None
#    gift = None
#    pmessage = None
#    name = None
#    form = NameForm()
#    if form.validate_on_submit():
#        name = form.name.data
#        address = form.address.data
#        gift = form.gift.data
#        pmessage = form.pmessage.data
#        #if old_name is not None and old_name != form.name.data:
#            #flash('Looks like you have changed your name!')
#        form.name.data = ''
#        form.address.data = ''
#        form.gift.data = ''
#        form.pmessage.data = ''
#        return redirect('/submit')
#    return render_template('index.html', form=form, name=name, address=address, gift=gift, pmessage=pmessage)
    
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
        gift = form.gift.data
        pmessage = form.pmessage.data
        #if old_name is not None and old_name != form.name.data:
            #flash('Looks like you have changed your name!')
        form.name.data = ''
        form.address.data = ''
        form.gift.data = ''
        form.pmessage.data = ''
        return redirect('/congrats')
    return render_template('submit.html', form=form, name=name, address=address, gift=gift, pmessage=pmessage)
    
@app.route('/congrats')
def congrats():
    return render_template('congrats.html')
    
@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    username = None
    password = None
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        form.username.data = ''
        form.password.data = ''
        return redirect
    return render_template('test.html')
    


if __name__ == '__main__':
    manager.run()
