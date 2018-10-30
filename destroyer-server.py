from flask import Flask, request
import os
import requests

app = Flask(__name__, static_url_path='/static')

@app.route('/auth')
def add_to_slack_button():
    return app.send_static_file('add_to_slack.html')


@app.route('/auth/redirect')
def handle_auth_redirect():
    print('hello log world')
    print(request)
    options = {
        'code': request.args.get('code'),
        'client_id': os.environ.get('SLACK_CLIENT_ID'),
        'client_secret': os.environ.get('SLACK_CLIENT_SECRET'),
        'redirect_uri': os.environ.get('REDIRECT_URI')
    }

    print(options)
    rsp = requests.get('https://slack.com/api/oauth.access', params=options)
    print(rsp)
    return (rsp.content, rsp.status_code, rsp.headers.items())


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
