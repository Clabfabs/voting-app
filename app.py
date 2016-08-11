from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from utils import connect_to_redis
import os
import socket
import random
import json
import requests

option_a = os.getenv('OPTION_A', "Batman")
option_b = os.getenv('OPTION_B', "Superman")
hostname = socket.gethostname()
app = Flask(__name__)

metrics_host = os.environ.get('METRICS_HOST');

@app.route("/", methods=['POST','GET'])
def hello():
	while True:
		try:	
			voter_id = request.cookies.get('voter_id')
			if not voter_id:
				voter_id = hex(random.getrandbits(64))[2:-1]

			vote = None

			if request.method == 'POST':
                requests.post(metrics_host + '/click', data={click: 1})
                vote = request.form['vote']
				data = json.dumps({'voter_id': voter_id, 'vote': vote})
				redis.rpush('votes', data)

			resp = make_response(render_template(
				'index.html',
				option_a=option_a,
				option_b=option_b,
				hostname=hostname,
				vote=vote,
			))
			resp.set_cookie('voter_id', voter_id)
			return resp
		except:
			redis = connect_to_redis(os.environ.get('REDIS_HOST'))

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)
