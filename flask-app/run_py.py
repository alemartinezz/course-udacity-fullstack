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
#!/usr/bin/env python3.6
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from orm_setup import Base, Caso
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from flask import session as login_session
import random
import string
from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import redirect
from flask import flash
from flask import jsonify


# flask app variable
app = Flask(__name__)

# Create session and connect with postgres Database
engine = create_engine("postgres://ale:aKjjyglc2@/law")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Obtain credentials from JSON file
CLIENT_ID = json.loads(open('client_secrets.json', 'r')
                       .read())['web']['client_id']
CLIENT_SECRET = json.loads(open('client_secrets.json', 'r')
                           .read())['web']['client_secret']
redirect_uris = json.loads(open('client_secrets.json', 'r')
                           .read())['web']['redirect_uris']
app.secret_key = CLIENT_SECRET

APPLICATION_NAME = "law-app-udacity"


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    """
    Function for log in endpoint.
    """

    # Detect login status
    login_status = None
    if 'email' in login_session:
        login_status = True

    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state

    return render_template('/login.html', STATE=state,
                           CLIENT_ID=CLIENT_ID, login_status=login_status)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """
    Function for connecting with the google account.
    """

    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already'
                                            'connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px; '
    output += ' -webkit-border-radius: 150px;-moz-border-radius:150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """
    Function for log out.
    """
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username']).encode('utf-8').strip()
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s'\
        % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect('/index')
    else:
        response = make_response(json.dumps('Failed to revoke token for\
        given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
    return response


# Endpoints
@app.route('/')
@app.route('/index')
def index():
    """
    Index endpoint. Calculate the percentages of cases and
    send variables to the template.
    """
    # Detect login status
    login_status = None
    if 'email' in login_session:
        login_status = True

    total = session.query(Caso).count()

    casos_penal = session.query(Caso).filter_by(categoria="penal")
    penal = casos_penal.count()
    penal = round(penal * 100 / total, 1)

    casos_cont_admin = session.query(Caso).filter_by(
        categoria="cont_administrativo")
    cont_admin = casos_cont_admin.count()
    cont_admin = round(cont_admin * 100 / total, 1)

    casos_der_civil = session.query(Caso).filter_by(categoria="derecho_civil")
    der_civil = casos_der_civil.count()
    der_civil = round(der_civil * 100 / total, 1)

    casos_familia = session.query(Caso).filter_by(categoria="familia")
    familia = casos_familia.count()
    familia = round(familia * 100 / total, 1)

    casos_laboral = session.query(Caso).filter_by(categoria="laboral")
    laboral = casos_laboral.count()
    laboral = round(laboral * 100 / total, 1)

    return render_template('index.html', penal=penal, laboral=laboral,
                           familia=familia, der_civil=der_civil,
                           cont_admin=cont_admin, login_session=login_session,
                           login_status=login_status)


# Functions for the categories.
@app.route('/penal')
def Penal():
    """
    Function for the category "penal". Send the cases of this
    category.
    """
    # Detect login status
    login_status = None
    if 'email' in login_session:
        login_status = True

    casos = session.query(Caso).filter_by(categoria="penal")

    total = session.query(Caso).count()
    penal = casos.count()
    penal = round(penal * 100 / total, 1)

    return render_template('/categorias/penal.html', casos=casos, total=total,
                           penal=penal, login_session=login_session,
                           login_status=login_status)


@app.route('/cont-administrativo')
def ContAdministrativo():
    """
    Function for the category "cont-administrativo". Send the cases of this
    category and the percentage.
    """
    # Detect login status
    login_status = None
    if 'email' in login_session:
        login_status = True

    casos = session.query(Caso).filter_by(categoria="cont_administrativo")

    total = session.query(Caso).count()
    cont_admin = casos.count()
    cont_admin = round(cont_admin * 100 / total, 1)

    return render_template('/categorias/cont-administrativo.html',
                           casos=casos, total=total, cont_admin=cont_admin,
                           login_session=login_session,
                           login_status=login_status)


@app.route('/der-civil')
def DerechoCivil():
    """
    Function for the category "Derecho Civil". Send the cases of this
    category and the percentage.
    """
    # Detect login status
    login_status = None
    if 'email' in login_session:
        login_status = True

    casos = session.query(Caso).filter_by(categoria="derecho_civil")

    total = session.query(Caso).count()
    der_civil = casos.count()
    der_civil = round(der_civil * 100 / total, 1)

    return render_template('/categorias/der-civil.html', casos=casos,
                           total=total, der_civil=der_civil,
                           login_session=login_session,
                           login_status=login_status)


@app.route('/familia')
def Familia():
    """
    Function for the category "Familia". Send the cases of this
    category and the percentage.
    """
    # Detect login status
    login_status = None
    if 'email' in login_session:
        login_status = True

    casos = session.query(Caso).filter_by(categoria="familia")

    total = session.query(Caso).count()
    familia = casos.count()
    familia = round(familia * 100 / total, 1)

    return render_template('/categorias/familia.html', casos=casos,
                           total=total,
                           familia=familia, login_session=login_session,
                           login_status=login_status)


@app.route('/laboral')
def Laboral():
    """
    Function for the category "Laboral". Send the cases of this
    category and the percentage.
    """
    # Detect login status
    login_status = None
    if 'email' in login_session:
        login_status = True

    casos = session.query(Caso).filter_by(categoria="laboral")

    total = session.query(Caso).count()
    laboral = casos.count()
    laboral = round(laboral * 100 / total, 1)

    return render_template('/categorias/laboral.html', casos=casos,
                           total=total, laboral=laboral,
                           login_session=login_session,
                           login_status=login_status)


# JSON endpoints for the categories.
@app.route('/laboral/JSON')
def LaboralJSON():
    """
    Endpoint JSON for the category "Laboral". Send the cases of this
    category in JSON format.
    """
    casos = session.query(Caso).filter_by(categoria="laboral")
    return jsonify(Caso=[i.serialize for i in casos])


@app.route('/penal/JSON')
def penalJSON():
    """
    Endpoint JSON for the category "Penal". Send the cases of this
    category in JSON format.
    """
    casos = session.query(Caso).filter_by(categoria="penal")
    return jsonify(Caso=[i.serialize for i in casos])


@app.route('/cont-administrativo/JSON')
def ContAdministrativoJSON():
    """
    Endpoint JSON for the category "Cont. Administrativo". Send
    the cases of this category in JSON format.
    """
    casos = session.query(Caso).filter_by(categoria="cont_administrativo")
    return jsonify(Caso=[i.serialize for i in casos])


@app.route('/der-civil/JSON')
def DerechoCivilJSON():
    """
    Endpoint JSON for the category "Derecho Civil". Send
    the cases of this category in JSON format.
    """
    casos = session.query(Caso).filter_by(categoria="derecho_civil")
    return jsonify(Caso=[i.serialize for i in casos])


@app.route('/familia/JSON')
def FamiliaJSON():
    """
    Endpoint JSON for the category "Familia". Send
    the cases of this category in JSON format.
    """
    casos = session.query(Caso).filter_by(categoria="familia")
    return jsonify(Caso=[i.serialize for i in casos])


# CRUD Functions
@app.route('/caso-<int:caso_id>')
def VerCaso(caso_id):
    """
    Function for displaying an individual case. Checking the login
    first for allowing the "edit" and "delete" buttons.
    """
    # Detect login status
    login_status = None
    if 'email' in login_session:
        login_status = True

    caso = session.query(Caso).filter_by(id=caso_id)
    return render_template('/caso/caso-ver.html', caso=caso,
                           login_session=login_session,
                           login_status=login_status)


@app.route('/caso-<int:caso_id>/JSON')
def VerCasoJSON(caso_id):
    """
    Endpoint JSON for an individual case. Send the response
    in JSON format.
    """
    caso = session.query(Caso).filter_by(id=caso_id)
    return jsonify(Caso=[i.serialize for i in caso])


@app.route('/nuevo-caso', methods=['GET', 'POST'])
def NuevoCaso():
    """
    Function for making a new case. Checking first if the user
    is logged in, then requesting the inputs.
    """
    # Detect login status
    login_status = None
    if 'email' in login_session:
        login_status = True

    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        new_case = Caso(nombre=request.form['input-nombre'],
                        categoria=request.form['input-categoria'],
                        creado=request.form['input-creado'],
                        juzgado=request.form['input-juzgado'],
                        actor=request.form['input-actor'],
                        demandado=request.form['input-demandado'],
                        precio=request.form['input-precio'],
                        descripcion=request.form['input-descripcion'],
                        status='Active')
        session.add(new_case)
        session.commit()
        flash("Case created successfully.")
        return redirect(url_for('index'))
    else:
        return render_template('/caso/caso-nuevo.html',
                               login_session=login_session,
                               login_status=login_status)


@app.route('/caso-<int:caso_id>/edit', methods=['GET', 'POST'])
def EditarCaso(caso_id):
    """
    Function for editing the case. Checking first if the user
    is logged in, then requesting the inputs.
    """
    # Detect login status
    login_status = None
    if 'email' in login_session:
        login_status = True

    if 'username' not in login_session:
        return redirect('/login')

    caso_editado = session.query(Caso).filter_by(id=caso_id).one()

    if request.method == 'POST':
        caso_editado.nombre = request.form['input-nombre']
        caso_editado.creado = request.form['input-creado']
        caso_editado.juzgado = request.form['input-juzgado']
        caso_editado.categoria = request.form['input-categoria']
        caso_editado.actor = request.form['input-actor']
        caso_editado.demandado = request.form['input-demandado']
        caso_editado.precio = request.form['input-precio']
        caso_editado.descripcion = request.form['input-descripcion']
        caso_editado.status = request.form['input-status']
        session.add(caso_editado)
        session.commit()
        flash("Case updated successfully.")
        return redirect(url_for('VerCaso', caso_id=caso_id))
    else:
        return render_template('/caso/caso-editar.html', caso=caso_editado,
                               login_session=login_session,
                               login_status=login_status)


@app.route('/caso-<int:caso_id>/delete', methods=['GET', 'POST'])
def BorrarCaso(caso_id):
    """
    Function for deleting the case. Checking first if the user
    is logged in, then commiting the delete.
    """
    # Detect login status
    login_status = None
    if 'email' in login_session:
        login_status = True

    if 'username' not in login_session:
        return redirect('/login')

    caso_borrar = session.query(Caso).filter_by(id=caso_id).one()

    if request.method == 'POST':
        session.delete(caso_borrar)
        session.commit()
        flash("Case deleted successfully.")
        return redirect(url_for('index'))
    else:
        return render_template('/caso/caso-borrar.html', caso=caso_borrar,
                               login_session=login_session,
                               login_status=login_status)


# execute the program
if __name__ == '__main__':
    """
    Function for running the app on any ip and port 8000.
    """
    app.secret_key = 'SUPER_SECRET_KEY'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)