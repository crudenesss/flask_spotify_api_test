from flask import redirect, request, session
import requests
import time, os
import random as rand
import string
from base64 import b64encode

def create_code(size):
	return ''.join(rand.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))

def get_token():
	token_url = 'https://accounts.spotify.com/api/token'
	client_id = os.environ.get('ID')
	client_secret = os.environ.get('SECRET')
	headers = {
		'Authorization': f'Basic {b64encode(bytes(client_id+":"+client_secret, "utf-8")).decode("ascii")}',
		'Content-Type': 'application/x-www-form-urlencoded'}
	body = {'grant_type': 'client_credentials'}
	post_response = requests.post(token_url, headers=headers, data=body)

	json = post_response.json()
	print(json)
	return json['access_token'], json['token_type'], json['expires_in']

def get_token_status(session):
	if time.time() > session['token_expiration']:
		payload = get_token()
		session['token'] = payload[0]
		session['token_expiration'] = time.time() + payload[2]
		return "Success"
	
def make_get_request(session, url, params=None):
	headers = {"Authorization": f"Bearer {session['token']}"}
	response = requests.get(url, headers=headers, params=params)

	if response.status_code == 200:
		return response.json()
	elif response.status_code == 401 and get_token_status(session) != None:
		return make_get_request(session, url, params)
	else:
		return None

def get_artist_info(session):
	if 'token' not in session.keys():
		token_data = get_token()
		session['token'] = token_data[0]
		session['token_expiration'] = time.time() + token_data[2]
	url = 'https://api.spotify.com/v1/artists/2n2RSaZqBuUUukhbLlpnE6'
	payload = make_get_request(session, url)

	if payload == None:
		return None

	return payload

def get_releases(session):
	if 'token' not in session.keys():
		token_data = get_token()
		session['token'] = token_data[0]
		session['token_expiration'] = time.time() + token_data[2]
	url = 'https://api.spotify.com/v1/browse/new-releases?country=US&limit=20'
	payload = make_get_request(session, url)

	if payload == None:
		return None

	return payload
		