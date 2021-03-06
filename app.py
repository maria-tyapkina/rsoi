from flask import Flask, redirect, request, jsonify
import requests
import json


app = Flask(__name__)
app.config.from_object('default_settings')
@app.route("/")
def hello():
    return "Hello world!"


@app.route("/no_auth")
def no_auth():
    g = requests.get("https://api.dailymotion.com/auth")
    return g.content

@app.route("/with_auth")
def with_auth():
    client_id = app.config['KEY']
    return redirect("https://www.dailymotion.com/oauth/authorize?" +
                    "&response_type=code&" +
                    "client_id={0}".format(client_id) +
                    "&state=123&redirect_uri=http://127.0.0.1:5001/oauth_callback")

@app.route("/oauth_callback", methods=['POST', 'GET'])
def oauth_callback():
    code = request.args.get("code")
    param = {'code': code, 'client_secret': app.config['SECRET'], 
             'grant_type': "authorization_code", 
             "redirect_uri":"http://127.0.0.1:5001/oauth_callback",
             "client_id" : app.config['KEY']}
    r = requests.post("https://api.dailymotion.com/oauth/token", param)
    '''token = r.json.get('access_token')
    header = {'Authorization': "Bearer {0}".format(token)}
    '''
    r = json.loads(r.text)
    token = r['access_token']
    g = requests.get("https://api.dailymotion.com/auth"+ "?access_token=" + token)
    return g.text

if __name__ == "__main__":
    app.run(port = 5001)





