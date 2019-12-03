#!/usr/bin/python3
# -*- coding: utf-8 -*-


from datetime import datetime
from flask import render_template, flash, redirect, url_for
from flask import request
from web_app import app
from web_app import db
from flask_login import current_user, login_user
from flask_login import logout_user, login_required
from werkzeug.urls import url_parse
from web_app.models import User, criar_primeiro_usuario
from web_app.forms import LoginForm
from web_app.forms import RegistrationForm
from web_app.forms import EditProfileForm
from web_app.forms import PostForm
from web_app.models import Comunicado
from web_app.forms import ResetPasswordRequestForm
from web_app.email import send_password_reset_email
from web_app.forms import ResetPasswordForm


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Cheque seu e-mail para instruções de como resetar sua senha')
        return redirect(url_for('login'))
    # Nessa instrucao nao é usado URL_FOR
    # Caso contrario, entraria em loop infinito!
    # Porque este comando chama uma funcao e nao um HTML
    return render_template('reset_password_request.html',
                           title='Resetar Senha',
                           form=form)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        # O parametro titulo é pego do formulario asssociado ao objeto: form.
        # Declarado acima
        comunicado = Comunicado(titulo=form.post.data, autor=current_user)
        db.session.add(comunicado)
        db.session.commit()
        flash('Sua postagem está disponível aos leitores!')
        # Pratica comum em respostas de formularios. 
        # Evitar erro ao atualizar pagina
        # Tecnica chamada: Padrao Post/Redirect/Get
        return redirect(url_for('index'))
    
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
    return render_template("index.html",
                           title='Página Principal',
                           form=form,
                           comunicados=posts.items,
                           next_url=next_url,
                           prev_url=prev_url)
    

@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Comunicado.query.order_by(Comunicado.dtCadastro.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html',
                           title='Navegar',
                           comunicados=posts.items,
                           prev_url=prev_url,
                           next_url=next_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    query = db.session.query(User).count()
    print('[ INFO ] Numero de usuarios:', query)
    if query == 0:
        criar_primeiro_usuario()
        # somente usar url_for quando chamar funcoes.
        # Nao serve para chamar arquivos HTML
        return render_template('info_usu_padrao.html')

    if current_user.is_authenticated:
        # Como esta usando url_for, 
        # quer dizer q esta chamando a funcao acima INDEX
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        #if user is None or user.password is None or not user.check_password(form.password.data):
        if user is None or not user.check_password(form.password.data):
            flash('Nome de usuário ou senha inválido')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Parabéns, você é um novo usuário registrado!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registrar', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Comunicado.query.order_by(Comunicado.dtCadastro.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) if posts.has_prev else None
    return render_template('user.html',
                           user=user,
                           posts=posts.items,
                           next_url=next_url,
                           prev_url=prev_url)

@app.before_request
def before_request():
    # Com a chamada IS_AUTHENTICATED, uma sessao do banco é aberta, entao,
    # podemos usar esta sessao para inserir dados nas "variaveis" dos models
    # e comitar a transacao
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Suas mudancas foram realizadas.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Usuário {} não encontrado.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('Você não pode seguir a si mesmo!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('Você está seguindo {}!'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Usuário {} não encontrado.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('Você nao pode seguir a si mesmo!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('Você não está seguindo {}.'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Sua senha foi resetada.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
