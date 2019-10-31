-- --------------------------------------------------------
-- DATABASE: CIRCULA_SETOR.DB
--
-- Tabelas que pertencem ao software: CIRCULA_SETOR
-- Autor: MuriloCunha - mcscunha@yahoo.com.br
-- Data: 31/10/2019
-- --------------------------------------------------------

create table usuario (
    id integer not null primary key autoincrement,
    usuario varchar(30),
    nome varchar(100),
    senha varchar(50),
    email varchar(100),
    data_cadastro date
);

create table setor (
    id integer not null primary key autoincrement,
    setor varchar(100),
    ativo varchar(1),
    data_cadastro date
);

create table comunicado (
    id integer not null primary key autoincrement,
    id_usuario integer,
    id_set_de integer,
    data_cadastro date,
    titulo varchar(100) not null,
    comunicado text not null,
    apagado varchar(1),
    foreign key (id_usuario) references usuario(id)
);

create table comunicado_setor (
    id integer not null primary key autoincrement,
    id_comunicado integer,
    id_setor integer
    data_lido date,
    hora_lido varchar(8),
    foreign key (id_comunicado) REFERENCES comunicado(id),
    foreign key (id_setor) REFERENCES setor(id)
);

create table log_comunicado (
    id integer not null primary key autoincrement,
    id_comunicado integer,
    id_usuario integer,
    data_cadastro date,
    hora_cadastro varchar(8),
    foreign key (id_usuario) references usuario(id),
    foreign key (id_comunicado) REFERENCES comunicado(id)
);