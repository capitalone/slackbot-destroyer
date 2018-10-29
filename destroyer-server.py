from flask import Flask, request

app = Flask(__name__, static_url_path='/static')

@app.route('/auth')
def add_to_slack_button():
    return app.send_static_file('add_to_slack.html')


@app.route('/auth/redirect')
def handle_auth_redirect():
    options = {
        'code': request.query.code,
        'client_id': os.environ('SLACK_CLIENT_ID'),
        'client_secret': os.environ('SLACK_CLIENT_SECRET'),
        'redirect_uri': os.environ('REDIRECT_URI')
    }
    return requests.get('https://slack.com/api/oauth.access', params=options)
