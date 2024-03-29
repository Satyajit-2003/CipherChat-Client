from app import app, cache, models
from app.socket import connect_to_server
from app.utils.keys import generate_keys, get_public_key, check_private_key, store_public_key
from app.utils.encryption import decrypt
from flask import render_template, request, redirect, url_for, flash
import requests

@app.route('/')
def index():
    if cache.get('token'):
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        flash("Please fill the form to register","info")
        return render_template('register.html')
    else:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        if password == confirm_password:
            if generate_keys(username) == 0:
                flash("User already exists","danger")
                return render_template('register.html')
            payload = {'username': username,
                        'password': password,
                        'email': email,
                        'public_key': get_public_key(username)}
            response = requests.request("POST", app.config['SERVER_API']+'/register',  data=payload)
            if response.status_code == 200:
                flash("Registered Sucessfully", "Success")
                return redirect(url_for('login'))
            else:
                flash("Email already exists","danger")
                return redirect(url_for('register'))
        else:
            flash("Password doesn't match","danger")
            return render_template('register.html')
    # username,email,password,confirm_password -> need to be added in the form

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
            return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        if check_private_key(username) == False:
            flash("Private key unavailable","danger")
            return render_template('login.html')        
        if username and password:               #username is not None and password is not None
            payload = { 'username' : username,
                       'password' : password}
            response = requests.request('POST',app.config['SERVER_API']+'/login', data=payload)
            # TODO: Store token from response if status_code == 200
            # Token stored in cookie
            if response.status_code == 200:
                cache.set('token', response.json()['token'])
                cache.set('username', username)
                resp = requests.request('POST', app.config['SERVER_API']+'/get_messages', data={'token': response.json()['token']})
                if resp.status_code == 200:
                    for message in resp.json():
                        message['message'] = decrypt(message['message'], username)
                        print(message)
                        models.add_message(message['sender'], message['message'], 0, message['timestamp'])
                return redirect(url_for('home'))           
            else:
                flash("Invalid credentials","danger")
                return render_template('login.html')

@app.route('/home', methods=['GET'])
def home():
    print(cache.get('token'))
    if cache.get('token'):
        connect_to_server()
        if request.args.get('user'):
            if get_public_key(request.args['user']) is None:
                resp = requests.request('GET', app.config['SERVER_API']+'/get_public_key?user='+request.args['user'])
                if resp.status_code == 200:
                    store_public_key(request.args['user'], resp.json()['public_key'])
            return render_template('home.html', username = [cache.get('username'), request.args['user']])
        return render_template('home.html', username = [cache.get('username'), ''])
    else:
        flash("Please login to continue","info")
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    if cache.has('token'):
        requests.request('POST', app.config['SERVER_API']+'/logout', data={'token': cache.get('token')})
        cache.delete('token')
        cache.delete('username')
    return redirect(url_for('login'))

@app.route('/get_users')
def get_users():
    if cache.get('token'):
        response = requests.request('POST', app.config['SERVER_API']+'/users', data={'token': cache.get('token')})
        print(response)
        return response.json(), 200
    else:
        return {'error': 'Unauthorized'}, 401

@app.route('/get_messages')
def get_messages():
    print(request.args.get('user'))
    if cache.get('token') and request.args.get('user'):
        print(request.args['user'])
        response = models.get_messages(request.args['user'])
        res = []
        print(cache)
        for message in response:
            res.append({'message': message.message, 'timestamp': message.timestamp, 'send': message.send})
        return {'messages': res}, 200
    else:
        return {'error': 'Unauthorized'}, 401