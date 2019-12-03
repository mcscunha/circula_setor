#!/usr/bin/python3
# -*- coding: utf-8 -*-


# Biblioteca padrao para pegar DATA e HORA do sistema
from datetime import date, datetime
# Biblioteca para instanciar o banco de dados
from web_app import db
# Bibliotecas para construcao do LOGIN
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from web_app import login
# Sobre Gravatar
from hashlib import md5
# Email
from time import time
import jwt
from web_app import app


# Se nao existir qualquer usuario no banco, crie um administrador
# com senha padrao
# Usuario: admin
# Senha  : admin
def criar_primeiro_usuario():
    sobre = '''
        Usuario criado automaticamente.
        Apenas para fazer o primeiro acesso ao sistema.
        Apos logar-se com ele, troque a senha ou crie outro e apague este.
        '''
    u = User(username='admin', about_me=sobre)
    u.set_password('admin')
    db.session.add(u)
    db.session.commit()


# Para saber qual usuario, a aplicacao faz uma busca no banco
# passando o ID do usuario
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# Tabela auxiliar para relacionamento MUITOS-MUITOS
# Um relacionametno na qual uma instancia DE UMA classe é
# referenciada para outra instancia da MESMA classe
# Isso é chamado relacao de auto referenciamento
# (self-referential relationship)
# Abaixo, estou relacionando USERS com USERS (leitores com escritores)
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    autor = db.relationship('Comunicado', backref='autor', lazy='dynamic')

    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic')
    
    def __repr__(self):
        return '<Usuario: {}>\n<E-mail: {}>'.format(self.username, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Nao pode passar NONE para o parametro PASSWORD, pois da erro
    # na hora do metodo CHECK_PASSWORD_HASH calcular o hash
    def check_password(self, password):
        if self.password_hash:
            return check_password_hash(self.password_hash, password)
        else:
            return None

    def avatar(self, size):
        if self.email:
            # ffef6a9fa57db9e8c0dfc21f7bf64309
            digest = md5(self.email.lower().encode('utf-8')).hexdigest()
            return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
                digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Comunicado.query.join(
                followers, 
                (followers.c.followed_id == Comunicado.idUsuario )
            ).filter(
                followers.c.follower_id == self.id
            )
        own = Comunicado.query.filter_by(idUsuario=self.id)
        return followed.union(own).order_by(Comunicado.dtCadastro.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Setor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    setor = db.Column(db.String(100), index=True, unique=True)
    ativo = db.Column(db.String(1))

    def __repr__(self):
        return '<Setor: {}>'.format(str(Setor.id) + ' - ' + Setor.setor)


class Comunicado(db.Model):
    data_hora_atual = datetime.now()
    data_atual = data_hora_atual.strftime('%d/%m/%Y')
    hora_atual = data_hora_atual.strftime('%H:%M')

    id = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('user.id'))
    idSetorOrigem = db.Column(db.Integer, db.ForeignKey('setor.id'))
    dtCadastro = db.Column(db.DateTime, default=data_hora_atual)
    titulo = db.Column(db.String(100), index=True)
    comunicado = db.Column(db.Text)
    apagado = db.Column(db.String(1))
    alteracoes = db.relationship(
        'LogComunicado', backref='alteracoes', lazy='dynamic')

    def __repr(self):
        return '<\n\tCadastro: {} - Titulo: {}' + \
               '\n\t Comunicado: {}\n>'.format(
                   self.dtCadastro, self.titulo, self.comunicado)


class ComunicadoSetor(db.Model):
    data_hora_atual = datetime.now()
    hora_atual = data_hora_atual.strftime('%H:%M')

    id = db.Column(db.Integer, primary_key=True)
    idComunicado = db.Column(db.Integer, db.ForeignKey('comunicado.id'))
    idSetor = db.Column(db.Integer, db.ForeignKey('setor.id'))
    hrLeitura = db.Column(db.Time, default=hora_atual)

    def __repr__(self):
        return '<ID Comunicado: {} - Setor: {} - Lido: {}>'.format(
            self.idComunicado, self.idSetor, self.hrLeitura
        )


class LogComunicado(db.Model):
    data_hora_atual = datetime.now()
    data_atual = data_hora_atual.strftime('%d/%m/%Y')
    hora_atual = data_hora_atual.strftime('%H:%M')

    id = db.Column(db.Integer, primary_key=True)
    idComunicado = db.Column(db.Integer, db.ForeignKey('comunicado.id'))
    idUsuario = db.Column(db.Integer, db.ForeignKey('user.id'))
    dtCadastro = db.Column(db.Date, default=data_atual)
    hrCadastro = db.Column(db.Time, default=hora_atual)

    def __repr__(self):
        return '<ID Comunicado: {}\n' + \
               ' ID Usuario: {}\n' + \
               ' Data Alteracao: {} - Hora Alteracao: {}'.format(
                   self.idComunicado,
                   self.idUsuario,
                   self.dtCadastro, self.hrCadastro
               )
