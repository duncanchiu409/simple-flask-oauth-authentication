from flask import Flask, url_for, jsonify, session, request, redirect
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.config['GOOGLE_ID'] = "id"
app.config['GOOGLE_SECRET'] = "secret"
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@app.route('/')
def hello():
    if 'google_token' in session:
        me = google.get('userinfo')
        return jsonify({"data": me.data})
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/login/callback')
def authorized():
    resp = google.authorized_response()

    # error handling
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    
    # setting up session
    session['google_token'] = resp['access_token']
    # me = google.get('userinfo')
    # return jsonify({"data": me.data})
    return resp

if __name__ == '__main__':
    app.run()