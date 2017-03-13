#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, aliased
import tables as my_tables
from users import example_users as my_users

print('Bem vindo ao meu exemplo de uso do SQLAlchemy!\n')
print('Vou começar criando um banco de dados temporário e criando duas tabelas\n')

#Engine of temporary db using SQLite
engine = create_engine('sqlite:///:memory:', echo=True)
Base = my_tables.base() #Pega o Base criado nas tabelas
Base.metadata.create_all(engine) #Cria as duas tabelas
print("Foram criadas as tabelas de usuários e de time. Agora vamos fazer a relação entre as duas.\n")
Base.metadata.create_all(engine) #Cria a relação entre as duas tabelas
print('Agora vamos criar a nossa sessão\n')
Session = sessionmaker(bind=engine)
session = Session()
print('Pronto, agora podemos criar alguns usuários...\n')
session.add_all(my_users)#Adicionado um dicionário de usuários
print('')
print('Bem, os usuários foram adicionados mas não foram salvos no BD.')
print('O session.new mostra que eles foram instanciados...\n')
print(session.new)
print('')
print('Agora vamos adicionar esses usuários no BD com session.commit\n')
session.commit() #Commit changes
print('')
print('Pronto! Tudo está salvo no banco! =D')
print('Vamos ver quem está no Banco? Pra isso vamos fazer uma query! \n')

for instance in session.query(my_tables.User).order_by(my_tables.User.id):
    print(instance.name)

print('Bem, vamos fazer uma search por um dos usuarios adicionados?? Mais uma query!\n')
user_ = session.query(my_tables.User).filter(my_tables.User.name.like('%lays%')).first()
user_.catch_phrase = "C++ e amor"

print('Bem pesquisei um user, e troquei seu catch phrase, pra ver alterações de usuários que estão no banco \n a gente usa o dirty\n')
print(session.dirty) #Print users that was changed but not commited
print('')
print('Vamos salvar? session.commit de novo!')
session.commit() #Commit changes
print('')
print('Agora vamos ver nossos usuários e seus catch phrases? =D\n')
user_alias = aliased(my_tables.User, name='user_alias')
for row in session.query(user_alias, user_alias.name, user_alias.catch_phrase).order_by(user_alias.id):
    print('\nName: ' + row.user_alias.name)
    print('Catch Phrase: ' + row.user_alias.catch_phrase)

print('\n Vamos começar a usar a relação que criamos...')
lays = session.query(my_tables.User).filter(my_tables.User.name.like('%lays%')).first()
if lays:
    lays.team = [my_tables.Team(team = 'Losys')]

toscano = session.query(my_tables.User).filter(my_tables.User.name.like('%toscano%')).first()
if toscano:
    toscano.team = [my_tables.Team(team='Web')]

print('Salvando o usuários agora com times...\n')
session.commit() #Commit changes
print('Vamos ver como nosso BD está?')
for u, a in session.query(my_tables.User, my_tables.Team).\
    filter(my_tables.User.id==my_tables.Team.user_id).all():
    print(u.name + ' esta no time ' + a.team)
print('\nPor hoje é só pessoal! \n')
