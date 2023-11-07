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
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from orm_setup import Base, Caso

engine = create_engine("postgres://ale:aKjjyglc2@/law")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Penal
caso1 = Caso(categoria="penal", creado='2018/2/19', status="Active", nombre="Fraud", juzgado="Criminal Court 22ª turn", actor="Ken Rosenberg", demandado="Jeffrey 'OG Loc' Cross", precio="12.500", descripcion="The client received a bounced check.")
session.add(caso1)
session.commit()

caso2 = Caso(categoria="penal", creado='2018/4/6', status="Active", nombre="Swindle", juzgado="Criminal Court 18ª turn", actor="David Parcerisa", demandado="Donkey Kong", precio="13.999", descripcion="The client was scammed by a fraudulent travel agency.")
session.add(caso2)
session.commit()

caso3 = Caso(categoria="penal", creado='2017/9/11', status="Active", nombre="Theft", juzgado="Criminal Court 18ª turn", actor="Tommy Vercetti", demandado="Lance Vance", precio="88.988", descripcion="The client's house was stolen all his belongings while he was on vacation.")
session.add(caso3)
session.commit()

caso4 = Caso(categoria="penal", creado='2018/4/6', status="Active", nombre="Homicide", juzgado="Criminal Court 10ª turn", actor="Sam Fisher", demandado="Solid Snake", precio="1.000", descripcion="The client's son was murdered in his house by a thief who came to steal.")
session.add(caso4)
session.commit()

caso5 = Caso(categoria="penal", creado='2016/10/20', status="Closed", nombre="Undue Appropriation", juzgado="Criminal Court 4ª turn", actor="Crash Bandicoot", demandado="Mario Bros", precio="24.876", descripcion="The client (boss) reports to his employee who improperly appropriates the salary settlement of the staff.")
session.add(caso5)
session.commit()


# Cont. Administrativo
caso6 = Caso(categoria="cont_administrativo", creado='2017/01/07', status="Active", nombre="Damages", juzgado="Administrative Court 4th turn", actor="Alex Mercer", demandado="Uruguaian State", precio="4.567", descripcion="The customer was rammed by an official car.")
session.add(caso6)
session.commit()

caso7 = Caso(categoria="cont_administrativo", creado='2019/2/18', status="Active", nombre="Damages", juzgado="Administrative Court 6ª turn", actor="Leon S. Kennedy", demandado="Swiss State", precio="2.566", descripcion="The client was billed with an undue amount by a state company providing services.")
session.add(caso7)
session.commit()


# Der. Civil
caso8 = Caso(categoria="derecho_civil", creado='2018/10/10', status="Active", nombre="Eviction", juzgado="Civil Court 4th turn", actor="Chris Redfield", demandado="Jill Valentine", precio="4.556", descripcion="The customer received a crash from an official vehicle.")
session.add(caso8)
session.commit()

caso9 = Caso(categoria="derecho_civil", creado='2019/02/19', status="Active", nombre="Foreclosure", juzgado="Civil Court 10th turn", actor="Hal Emmerich", demandado="Naomi Watson", precio="103.766", descripcion="The client delivers his property as collateral in a loan to the republic bank. Then he did not pay the debt and the bank started taking steps to get his property.")
session.add(caso9)
session.commit()

caso10 = Caso(categoria="derecho_civil", creado='2019/08/02', status="Closed", nombre="Seizure", juzgado="Juzgado Civil de 8ª turno", actor="Nathan Drake", demandado="Tempeney", precio="34.766", descripcion="A person made a loan to a financial company and the company established a seizure on their assets.")
session.add(caso10)
session.commit()


# Familia
caso11 = Caso(categoria="familia", creado='2018/12/12', status="Active", nombre="Divorce", juzgado="Family Trial Court 3rd turn", actor="Leon Pinkus", demandado="Jim Carrey", precio="234.344", descripcion="Two spouses are divorcing because of the reason: quarrels and disputes.")
session.add(caso11)
session.commit()

caso12 = Caso(categoria="familia", creado='2018/12/04', status="Active", nombre="Alimony", juzgado="Family Trial Court 8th turn", actor="The Sims", demandado="Master Chief", precio="43.000", descripcion="The client (mother) claims the father's pension for his son.")
session.add(caso12)
session.commit()

caso13 = Caso(categoria="familia", creado='2018/10/16', status="Active", nombre="Succession of goods", juzgado="Family Trial Court 6th turn", actor="Lara Croft", demandado="Vault Boy", precio="22.999", descripcion="The owner of a house died leaving heirs with rights to the property.")
session.add(caso13)
session.commit()

caso14 = Caso(categoria="familia", creado='2018/07/02', status="Closed", nombre="Injuries", juzgado="Specialized Family Court 4th turn", actor="Solid Snake", demandado="Trevor Phillips", precio="11.000", descripcion="The spouse executed physical abuse against his wife and children.")
session.add(caso14)
session.commit()


# Laboral
caso15 = Caso(categoria="laboral", creado='2018/03/23', status="Active", nombre="Abusive dismissal", juzgado="Labor Court 17th turn", actor="Minecraft Steve", demandado="Kratos", precio="7.999", descripcion="The client was dismissed without respecting the labor rights of the same.")
session.add(caso15)
session.commit()

caso16 = Caso(categoria="laboral", creado='2018/04/28', status="Active", nombre="No overtime payment", juzgado="Labor Court 7th turn", actor="Donald Duck", demandado="Rich Uncle Pennybags", precio="2.999", descripcion="The client usually worked two extra hours per day which were not compensated in their salary at the end of the month.")
session.add(caso16)
session.commit()


print ("data inserted!")