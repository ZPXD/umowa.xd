from flask import Flask, render_template, request, redirect, url_for

import flask_wtf
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField, IntegerRangeField
from wtforms.validators import DataRequired

from flask_bootstrap import Bootstrap

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import LoginManager, UserMixin
from flask_login import login_required, current_user, login_user, logout_user

import os
import random
from datetime import datetime


here = os.getcwd()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/db/xd.db'.format(here)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = ':)'

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager(app)



# Main

@app.route('/')
def index():
    return render_template("index.html")


# Checker

@app.route('/sprawdz_umowe')
def sprawdz_umowe():
    return render_template("sprawdzumowe.html")

@app.route('/sprawdz_link')
def sprawdz_link():
    return render_template("sprawdz_link.html")

@app.route('/sprawdz_plik')
def sprawdz_plik():
    return render_template("sprawdz_plik.html")

@app.route('/sprawdz_tekst')
def sprawdz_tekst():
    return render_template("sprawdz_tekst.html")


# Info

@app.route('/diablochrony')
def diablochrony():
    return render_template("diablochrony.html")


# Flourish

@app.route('/umowmysie', methods=["GET", "POST"])
def umowmy_sie():
    form = UmowmysieForm()
    if form.validate_on_submit():

        agreement = Agreement(
            title = form.title.data, 
            who = form.who.data, # username integration [GUARDIAN]
            who2 = form.who2.data, # username integration
            #who_more = more who - list.
            action_if_not_fulfilled=form.action_if_not_fulfilled.data, 
            other_if_fulfileled=form.other_if_fulfileled.data, 
            action_if_fulfilled=form.action_if_fulfilled.data,
            other_if_not_fulfilled = form.other_if_not_fulfilled.data,
            witness = form.witness.data,
            public = form.public.data,
        )
        db.session.add(agreement)
        db.session.commit()

        return redirect( url_for('index'))

    return render_template("umowmysie.html", form=form)


@app.route('/najnowsze_umowy', methods=["GET", "POST"])
def newest_agreements():
    agreements = Agreement.query.all()
    return render_template("najnowsze_umowy.html", agreements=agreements)

def create_link():
    link = None



# Spotkania

@app.route('/spotkania')
def meetings():

    form = Ready()
    if form.validate_on_submit():
        return redirect('create_meeting')

    if current_user.is_authenticated:
        your_meetings = Meetings.query.filter(Meetings.who.contains(current_user.name))

    return render_template("meetings.html")

@app.route('/spotkanie/<int:meeting_id>')
def meeting(meeting_id):

    form = SendInvitation()
    if form.validate_on_submit():
        pass
        # send

    if current_user.is_authenticated:

        form = AddModifyMeetingData()
        if form.validate_on_submit():

            # I JOIN / IDK / IDKYET / NO
            
            joining = form.joining.data
            who = form.who.data
        
            when_decide = form.who.data
            decide_miscs = form.who.data

            t1_data = form.t1_date.data
            t1_time = form.t1_time.data
            t1_misc = form.t1_misc.data

            t2_data = form.t1_date.data
            t2_time = form.t1_time.data
            t2_misc = form.t1_misc.data

            t3_data = form.t1_date.data
            t3_time = form.t1_time.data
            t3_misc = form.t1_misc.data

            t4_data = form.t1_date.data
            t4_time = form.t1_time.data
            t4_misc = form.t1_misc.data

            t5_data = form.t1_date.data
            t5_time = form.t1_time.data
            t5_misc = form.t1_misc.data


    return render_template("meeting.html")


@app.route('/stworz_spotkanie', methods=["GET", "POST"])
def create_meeting():

    form = CreateMeeting()
    if form.validate_on_submit():
        meeting_title = form.meeting_title.date
        meeting_info = form.meeting_info.date

        
        # Possibilities:
        # Range


        

    return render_template("create_meeting.html")


# Randki

@app.route('/umowmysienarandke', methods=["GET", "POST"])
def umowmysienarandke():
    form = RandkaForm()
    if form.validate_on_submit():
        where = form.where.data
        when = form.when.data
        answerstyle = form.answerstyle.data
        home_or_nature = form.home_or_nature.data
        heya = form.heya.data
        data = 'woah'
        data += '\n'.join([where, when, answerstyle, home_or_nature, heya])
        send_paperplain(data)
    return render_template("umowmysienarandke.html", form=form)

def send_paperplain(data):
    with open('woah.txt', 'w') as f:
        f.write(data)


# Login

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    return user

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user:
            if user.check_password(password):
                login_user(user, force=True)
                return redirect( url_for('index'))
        else:
            return "user not found"

    return render_template("login.html", form=form)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        if User.query.filter_by(email=email).first():
            return 'taki email już istnieje'

        user = User(name=name, email=email, password=password)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return redirect( url_for('index'))
    return render_template("signup.html", form=form)

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return render_template("logout.html")


@login_required
@app.route('/profile/<name>')
def user(name):
    if name == current_user.name:
        return "ok"
    else:
        return "no"


# DB Models

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    join_date = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    password = db.Column(db.String(120))

    def set_password(self,password):
        self.password = generate_password_hash(password)
     
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.name)

class Agreement(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    last_update = db.Column(db.DateTime)

    title = db.Column(db.String(120))
    agree_to = db.Column(db.String(120))

    who = db.Column(db.String(120))
    who2 = db.Column(db.String(120))
    action_if_not_fulfilled = db.Column(db.String(120))
    other_if_fulfileled = db.Column(db.String(120))
    action_if_fulfilled = db.Column(db.String(120))
    other_if_not_fulfilled = db.Column(db.String(120))
    witness = db.Column(db.String(120))
    public = db.Column(db.String(120))

    date = None

    def __repr__(self):
        return '<Agreement {}>'.format(self.agree_to)



@app.before_first_request
def create_all():
    if not 'db' in os.listdir():
        os.mkdir('db')  
    db.create_all()


# Forms

class UmowmysieForm(FlaskForm):
    who = StringField(validators=[DataRequired()])
    who2 = StringField(validators=[DataRequired()])

    title = StringField(validators=[DataRequired()])
    agree_to = TextAreaField(validators=[DataRequired()])

    actions_if_not_fulfilled = [
        ('Czyszczę buty', 'Czyszczę buty'),
        ('Wrzucam publicznego posta', 'Wrzucam publicznego posta'),
        ('Przelewam X na konto fundacji pomocy', 'Przelewam X na konto fundacji pomocy'),
        ('Szkoda. Nic.', 'Szkoda. Nic.'),
        ('Inne (napisz poniżej)', 'Inne (napisz poniżej)'),
    ]
    
    actions_if_fulfilled = [
        ('Wypijmy szklankę wody/soku na zdrowie :)', 'Wypijmy szklankę wody/soku na zdrowie :)'),
        ('Zróbmy komuś fajną niespodziankę', 'Zróbmy komuś fajną niespodziankę'),
        ('+1 :) dawaj dalej', '+1 :) dawaj dalej')
    ]
    
    action_if_not_fulfilled = SelectField(choices=actions_if_not_fulfilled)
    other_if_fulfileled = StringField(validators=[DataRequired()])

    action_if_fulfilled = SelectField(choices=actions_if_fulfilled)
    other_if_not_fulfilled = StringField(validators=[DataRequired()])

    witness = StringField(validators=[DataRequired()])
    public = BooleanField()

    button = SubmitField('umawiamy się')


class RandkaForm(FlaskForm):
    where = StringField(validators=[DataRequired()])
    when = StringField(validators=[DataRequired()])
    answerstyle = StringField(validators=[DataRequired()])
    home_or_nature = StringField(validators=[DataRequired()])
    heya = StringField(validators=[DataRequired()])
    button = SubmitField(':**')

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('hasło', validators=[DataRequired()])
    button = SubmitField('zaloguj się')

class SignupForm(FlaskForm):
    name = StringField('nazwa użytkownika', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = StringField('hasło', validators=[DataRequired()])
    confirm_password = StringField('powtórz hasło', validators=[DataRequired()])
    button = SubmitField('załóż konto')


# Errors

@app.errorhandler(404)
def handle_404(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def handle_500(e):
    return render_template('500.html'), 500


if __name__=="__main__":
    app.run(debug=True)