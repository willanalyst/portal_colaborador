from flask import Flask, redirect, url_for, session, request, render_template
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2.rfc6749.errors import MismatchingStateError
import os

# Desativa HTTPS para desenvolvimento local
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = app = Flask(__name__, static_folder='assets')
app.secret_key = '1a862170-dbe6-4b51-b14e-a0ce25bd0a71'

CLIENT_ID = '4f188be3-1bc8-404d-bae5-79d3c89702eb'
CLIENT_SECRET = 'Z1M8Q~je4Y3yyQL.krKMhShRjZnos.sVenxSeaER'
AUTHORITY_URL = 'https://login.microsoftonline.com/02676efc-fb2b-4ef8-beee-ed6c67c36249'
AUTH_ENDPOINT = '/oauth2/v2.0/authorize'
TOKEN_ENDPOINT = '/oauth2/v2.0/token'
REDIRECT_URI = 'http://localhost:5000/getAToken'
SCOPE = ['User.Read', 'openid', 'profile', 'email', 'User.ReadBasic.All']

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/auth',methods=['GET', 'POST'])
def login():
    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
    authorization_url, state = oauth.authorization_url(AUTHORITY_URL + AUTH_ENDPOINT)

    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route('/getAToken')
def get_a_token():
    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE, state=session.get('oauth_state'))
    
    try:
        token = oauth.fetch_token(AUTHORITY_URL + TOKEN_ENDPOINT, client_secret=CLIENT_SECRET, authorization_response=request.url)
        session['oauth_token'] = token
        return render_template('index.html')
    except MismatchingStateError:
        return 'Erro de estado CSRF: O estado na solicitação e na resposta não corresponde.'


@app.route('/logout')
def logout():
    # Limpar a sessão
    session.clear()

    # Definir a URL de redirecionamento após o logout para a tela de login do seu aplicativo
    post_logout_redirect_uri = url_for('home', _external=True)

    # URL de logout do Microsoft AD
    logout_url = f'https://login.microsoftonline.com/common/oauth2/logout?post_logout_redirect_uri={post_logout_redirect_uri}'

    # Redirecionar para a URL de logout do Microsoft AD
    return redirect(logout_url)



if __name__ == '__main__':
    app.run(debug=True)
