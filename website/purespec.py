from flask import Blueprint, render_template, request, flash, jsonify,redirect,url_for
from flask_login import login_required, current_user
import requests
import json

purespec = Blueprint('purespec', __name__,url_prefix='/purespec')

S_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2ZmYxMDU2ZTNiMDYwNjViNjdjZWVhYyIsInVzcl9pZCI6IjQxNjEiLCJpYXQiOjE3Mjc5OTE4OTR9.pI1elr6KDOHPbakvZ2aKjL-OR-b_iJqIUDA5Yx94Jrs'
S_BASE_URL='http://staging.spectrumsurveys.com/suppliers/v2/'

L_API_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2ZmYxMDU2ZTNiMDYwNjViNjdjZWVhYyIsInVzcl9pZCI6IjQxNjEiLCJpYXQiOjE3Mjc5OTE4OTR9.pI1elr6KDOHPbakvZ2aKjL-OR-b_iJqIUDA5Yx94Jrs'
L_BASE_URL='http://staging.spectrumsurveys.com/suppliers/v2/'

is_Live=False

if is_Live:
    API_KEY=L_API_KEY
    BASE_URL=L_BASE_URL
else:
    API_KEY=S_API_KEY
    BASE_URL=S_BASE_URL




session = requests.Session()
# these are sent along for all requests
session.headers['x-access-token'] = API_KEY
session.headers['Accept'] = "application/json"


@purespec.route('/home', methods=['GET'])
@login_required
def home():
    url = BASE_URL+'surveys?reg=both'
    response = session.get(url)
    data = json.loads(response.content.decode('UTF-8'))
    print(data)
    return render_template("home_pure.html", user=current_user, sdata=data)
