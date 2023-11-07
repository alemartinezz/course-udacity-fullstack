---
author: No author.
tags:
  - knowledge
  - comp-sci
  - projects
  - FullStack Developer - Udacity
  - UdacityFullstack_FlaskApp
description: No description.
---
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Caso(Base):
    __tablename__ = 'caso'
   
    id = Column(Integer, primary_key=True)
    creado = Column(Date(), nullable=True)
    status = Column(String(20), default="Active", nullable=True)
    nombre = Column(String(250), nullable=False)
    precio = Column(String(8))
    categoria = Column(String(100), nullable=True)
    juzgado = Column(String(100), nullable=True)
    actor = Column(String(100), nullable=False)
    demandado = Column(String(100), nullable=True)
    descripcion = Column(String(400), nullable=False)

    @property
    def serialize(self):
        return {
            'name': self.nombre,
            'description': self.descripcion,
            'id': self.id,
            'price': self.precio,
            'actor': self.actor,
            'defendant': self.demandado,
            'category': self.categoria,
            'court': self.juzgado,
            'date': self.creado,
            'status': self.status,
        }

engine = create_engine("postgres://ale:aKjjyglc2@/law")
Base.metadata.create_all(engine)