from flask import Blueprint, render_template, request, flash, jsonify,redirect,url_for
from flask_login import login_required, current_user
import requests
import json

views = Blueprint('views', __name__)

S_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2YmNiZTg5MTlhOGQ2ODZhZTEwYWI2NSIsInVzcl9pZCI6NTkyOCwidXNyX3R5cGUiOiJzdXBwbGllciIsImlhdCI6MTcyMzY0NTU3N30.GtwamU5UQO3vD7OBGIrImhLRB7k1aOJ2w4UBjava3wk'
S_BASE_URL='https://stagediysamplingapi.innovatesample.com/api/v2/supply/'

L_API_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2ZDIyNzk5ODllYmUxNmQ3MjE3M2VjZCIsInVzcl9pZCI6MTE4MCwidXNyX3R5cGUiOiJzdXBwbGllciIsImlhdCI6MTcyNTA0ODcyOX0.Bsj1PPO7PCXpw6ZBE9sm0ANeW_HeHyolD776zA_miW0'
L_BASE_URL='https://supplier.innovatemr.net/api/v2/supply/'

is_Live=True

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



@views.route('/', methods=['GET'])
@login_required
def home():
    response_data=1
    return render_template("home.html", user=current_user)

@views.route('/getLiveSurvey',methods=['POST'])
@login_required
def getLiveSurvey():
    c_code=request.form.get('countryCode')
    l_code=request.form.get('languageCode')
    url = BASE_URL+'getAllocatedSurveys'
    session.headers['countryCode'] = c_code
    session.headers['languageCode'] = l_code
    response = session.get(url)
    data = json.loads(response.content.decode('UTF-8'))
    return render_template("all_project.html", user=current_user, sdata=data)



    #
    # if request.method == 'POST':
    #     note = request.form.get('note')#Gets the note from the HTML
    #
    #     if len(note) < 1:
    #         flash('Note is too short!', category='error')
    #     else:
    #         new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note
    #         db.session.add(new_note) #adding the note to the database
    #         db.session.commit()
    #         flash('Note added!', category='success')



@views.route('/getdetails',methods=['GET'])
@login_required
def getdetails():
    PID = request.args.get("pid")  #
    url = BASE_URL+'getAllocatedSurveysBySurveyId/'+PID
    response = session.get(url)
    data = json.loads(response.content.decode('UTF-8'))
    return render_template("project.html", user=current_user, sdata=data)


@views.route('/getredirect',methods=['GET'])
@login_required
def getredirect():
    PID = request.args.get("pid")  #
    url = BASE_URL+'surveySpecificRedirects/'+PID
    response = session.get(url)
    data = json.loads(response.content.decode('UTF-8'))
    return render_template("redirects.html", user=current_user, sdata=data,d_PID=PID)



@views.route('/setredirect',methods=['POST'])
@login_required
def setredirect():
    if request.method == 'POST':
        pid = request.form.get('d_PID')
        sUrl = request.form.get('sUrl')
        fUrl = request.form.get('fUrl')
        tUrl = request.form.get('tUrl')
        oUrl = request.form.get('oUrl')

        if len(pid)<2:
            flash('Invalid Project id.', category='error')
        elif len(sUrl)<2:
            flash('Please provide valid URL for Success.', category='error')
        elif len(fUrl)<2:
            flash('Please provide valid URL for Failed.', category='error')
        elif len(tUrl)<2:
            flash('Please provide valid URL for Termination.', category='error')
        elif len(oUrl)<2:
            flash('Please provide valid URL for overQuota.', category='error')

        url = BASE_URL + 'setRedirectionForSurvey/' + pid
        mydata = {}
        mydata['sUrl'] =sUrl
        mydata['fUrl'] =fUrl
        mydata['oUrl'] =oUrl
        mydata['tUrl'] =tUrl
        session.headers['Content-Type'] = "application/json"
        session.headers['Accept'] = "application/json"

        response = session.put(url, json=mydata)
        data = json.loads(response.content.decode('UTF-8'))
        if response.status_code == 200:
            flash('Redirect URL were Set correctly', category='success')
        else:
            f_error=f'Failure in updating the recirects \n Error={data}'
            flash(f_error,category='alert')

        return redirect(url_for('views.getredirect',pid=pid))

