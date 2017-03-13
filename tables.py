#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
     __tablename__ = 'users'

     id = Column(Integer, primary_key=True)
     name = Column(String)
     mail = Column(String)
     profession = Column(String)
     catch_phrase = Column(String)

     def __repr__(self):
        return "<User(name='%s', mail='%s', profession='%s' ,catch_phrase='%s')>" % (
                             self.name, self.mail, self.profession ,self.catch_phrase)

class Team(Base):
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    team = Column(String, nullable=False)
    user = relationship("User", back_populates="team")
    def __repr__(self):
        return "<Team(team='%s')>" % self.team

User.team = relationship("Team", order_by=Team.id, back_populates ="user")

def base():
    return Base
