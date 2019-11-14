
from web_app import db
from datetime import date, datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    autor = db.relationship('Comunicado', backref='autor', lazy='dynamic')

    def __repr__(self):
        return '<Usuario: {}>\n<E-mail: {}>'.format(self.username, self.email)


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
    dtCadastro = db.Column(db.Date, default=data_atual)
    titulo = db.Column(db.String(100), index=True)
    comunicado = db.Column(db.Text)
    apagado = db.Column(db.String(1))
    alteracoes = db.relationship('LogComunicado', backref='alteracoes', lazy='dynamic')

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

    id = db.Column(db.Integer, primary_key= True)
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