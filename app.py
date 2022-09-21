from crypt import methods
from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from random import randint, choice, sample
from surveys import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'something'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def home_page():
    """Shows home page"""
    return render_template('home.html', satisfaction_survey=satisfaction_survey)


@app.route('/question/<questionID>')
def get_question(questionID):
    """ Gets the question from the survey """
    if len(responses) != int(questionID):
        flash("You must answer this question before advancing.")
        return redirect('/question/' + str(len(responses)))
        # return None
    return render_template('question.html',
                           satisfaction_survey=satisfaction_survey, questionID=questionID)


@app.route('/answer/<questionID>', methods=['POST'])
def post_answer(questionID):
    """ Looks for what question should be asked and records the answer to a list """
    if int(questionID) != len(responses):
        redirect('/question/' + str(questionID))
    responses.append(request.form['rdoQuestion'])
    session['responses'] = responses
    if int(questionID) < len(satisfaction_survey.questions) - 1:
        nextID = int(questionID) + 1
        return redirect('/question/' + str(nextID))
    else:
        return redirect('/thank-you')


@app.route('/show_survey')
def get_survey():
    """ Shows the survey page """
    return render_template('showSurvey.html', satisfaction_survey=satisfaction_survey)


@app.route('/thank-you')
def thank_you():

    return render_template('thankYou.html', responses=responses)


@app.route('/set_session', methods=['post'])
def set_session():
    responses.clear()
    session['responses'] = []
    return redirect('/question/0')
