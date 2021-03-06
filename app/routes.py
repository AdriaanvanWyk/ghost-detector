from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from app import app, db
from app.models import User, Ghost, GhostType, GhostCode
from app.forms import LoginForm, RegistrationForm, GhostForm
from random import randint, uniform


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('ghosts'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('ghosts'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('ghosts'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/ghosts', methods=['GET', 'POST'])
def ghosts():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user_id = User.query.filter_by(username=current_user.username).with_entities(User.id)
    ghost_types = GhostType.query.all()
    my_ghosts = Ghost.query.filter_by(user_id = user_id)
    for ghost in my_ghosts:
        ghost.type_id = GhostType.query.filter_by(id=ghost.type_id).with_entities(GhostType.name)
    return render_template('ghosts.html', title='Ghosts', ghosts=my_ghosts)

@app.route('/addghost', methods=['GET', 'POST'])
def addghost():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = GhostForm()
    if form.validate_on_submit():
        code_record = GhostCode.query.filter_by(code=form.code.data).first()
        code = code_record.code
        db.session.delete(code_record)
        user_id = User.query.filter_by(username=current_user.username).with_entities(User.id)
        new_ghost = Ghost(user_id = user_id, type_id = randint(1, 3), height = randint(20, 200), weight = round(uniform(1, 15), 2))
        db.session.add(new_ghost)
        db.session.commit()
        flash('Added new Ghost to Collection!')
    return render_template('addghost.html', title='Add Ghost', form=form)
