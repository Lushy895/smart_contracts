from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from app.models import db, User
from app.forms import LoginForm, RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Login failed. Check your credentials.', 'danger')
    return render_template('login.html', form=form)

@app.route('/contracts/create', methods=['GET', 'POST'])
@login_required
def create_contract():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        contract = Contract(title=title, content=content, user_id=current_user.id)
        db.session.add(contract)
        db.session.commit()
        flash('Contract created!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('contract_create.html')
