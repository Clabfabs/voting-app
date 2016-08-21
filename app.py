from __future__ import print_function

from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import redirect
from utils import connect_to_redis
import sys
import os
import socket
import random
import json
import requests

option_a = os.getenv('OPTION_A', "Batman")
option_b = os.getenv('OPTION_B', "Superman")
hostname = socket.gethostname()
app = Flask(__name__)

metrics_url = os.environ.get('METRICS_URL')

region = 'us'


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


@app.route("/", methods=['POST', 'GET'])
def hello():
    while True:
        try:
            voter_id = request.cookies.get('voter_id')
            if not voter_id:
                voter_id = hex(random.getrandbits(64))[2:-1]

            vote = None

            if request.method == 'POST':
                vote = request.form['vote']
                data = json.dumps({'voter_id': voter_id, 'vote': vote})
                redis.rpush('votes', data)
                try:
                    requests.post('http://' + metrics_url + '/v1/clicks', data={'origin': region})
                except requests.exceptions.RequestException:
                    eprint('Metric POST request not possible. Did you set METRIC_URL correctly?')



            resp = make_response(render_template(
                'index.html',
                option_a=option_a,
                option_b=option_b,
                hostname=hostname,
                vote=vote,
                region=region.upper()
            ))
            resp.set_cookie('voter_id', voter_id)
            return resp
        except:
            redis = connect_to_redis(os.environ.get('REDIS_HOST'))


@app.route("/regionswitch", methods=['POST'])
def regionswitch():
    global region

    if region == 'us':
        region = 'eu'
    elif region == 'eu':
        region = 'us'
    else:
        region = 'us'

    print('region switched to ' + region + '!')

    return redirect('/')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
