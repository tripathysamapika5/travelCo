import math

from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import os
from flask import flash

from configs import AppFactory
from models import modelService, Users, Posts

from flask import render_template, request, redirect, url_for
from datetime import datetime

from werkzeug.utils import secure_filename

import json

################ initialising databasees #################
from configs import db;
app = AppFactory.getApp(__name__)
db.init_app(app)
modelService.createDatabase()
socketio = SocketIO(app)
#modelService.initialiseUsers()
#modelService.initialisePosts()


################ Endpoints #################

@app.route('/')
def route_user_home():  # put application's code here
    return render_template('home_page.html')


@app.route('/login', methods=['GET', 'POST'])
def route_login():
    emailId = request.args.get("email")
    password = request.args.get("pwd")

    if emailId is not None:
        actualPassword = db.session.query(Users).filter_by(email=emailId)[0].__dict__.get('password')

        if (actualPassword == password):
            return redirect(url_for('route_plan_your_trip', emailId=emailId))
        else:
            return render_template('login.html', errorMessage="Login Failed !!!")

    return render_template('login.html')


@app.route('/user-home-page', methods=['GET', 'POST'])
def route_user_home_page():
    emailId = request.args.get('emailId')

    name = db.session.query(Users).filter_by(email=emailId)[0].__dict__.get('name')
    activities = db.session.query(Posts).all()

    newActivities = []

    for activity in activities:
        newActivity = vars(activity)
        newActivity['activities'] = json.loads(newActivity.get('activities'))
        newActivity['memberEmails'] = list(set(json.loads(newActivity.get('memberEmails'))))
        del newActivity['_sa_instance_state']
        newActivity['groupSize'] = len(newActivity.get('memberEmails')) + 1
        newActivity['isPrimary'] = newActivity.get('primaryEmail') == emailId
        newActivity['isMember'] = emailId in newActivity['memberEmails']
        newActivity['isNonMember'] = newActivity['isPrimary'] == False and newActivity['isMember'] == False
        newActivity['attachments'] = json.loads(newActivity.get('attachments'))

        newAttachments = newActivity.get('attachments')

        message = getInsight(newActivity.get('primaryEmail'), newAttachments)

        newActivity['message'] = message

        newActivities.append(newActivity)

    return render_template('user_home_page.html', name=name, activities=newActivities, emailId=emailId)


@app.route('/plan-your-trip', methods=['GET', 'POST'])
def route_plan_your_trip():
    print("values",request.args )
    print("values",request.form )
    emailId = request.args.get('emailId')

    name = db.session.query(Users).filter_by(email=emailId)[0].__dict__.get('name')
    activities = db.session.query(Posts).all()


    newActivities = []

    if (request.args.get('toLocation') is not None):
        tripStartDate = request.args.get('tripStartDate')
        tripEndDate = request.args.get('tripEndDate')
        fromLocation = request.args.get('fromLocation')
        toLocation = request.args.get('toLocation')
        activities = request.args.getlist('plannedActivity')
        ageGroup = request.args.get('ageGroup')

        print(tripStartDate, tripEndDate, fromLocation, toLocation, activities)

        posts = db.session.query(Posts).all()

        newPosts = []

        for post in posts:
            newPost = vars(post)
            newPost['activities'] = json.loads(newPost.get('activities'))
            newPost['memberEmails'] = list(set(json.loads(newPost.get('memberEmails'))))
            del newPost['_sa_instance_state']
            newPost['groupSize'] = len(newPost.get('memberEmails')) + 1
            newPost['isPrimary'] = newPost.get('primaryEmail') == emailId
            newPost['isMember'] = emailId in newPost['memberEmails']
            newPost['isNonMember'] = newPost['isPrimary'] == False and newPost['isMember'] == False
            newPost['attachments'] = json.loads(newPost.get('attachments'))


            newPost['userMembers'] = eval(newPost.get('userMembers'))
            msg1 = getInsightFromUserMebers(newPost['userMembers'] )
            newPost['message1'] = msg1

            newAttachments = newPost.get('attachments')

            message = getInsight(newPost.get('primaryEmail'), newAttachments)

            newPost['message'] = message

            totalScore = 8 + 3 + len(newPost['activities']) + 1

            score = getScoreFromaAttachments(newPost.get('primaryEmail'), newAttachments)

            delta = datetime.strptime(tripStartDate, '%Y-%m-%d').date() - datetime.strptime(
                newPost.get('tripStartDate'), '%Y-%m-%d').date()
            if abs(delta.days) <= 15:
                score += 1

            if toLocation == newPost.get('destinationLocation'):
                score += 1

            if fromLocation == newPost.get('fromLocation'):
                score += 1

            if newPost['groupSize'] > 1:
                score += 1

            for activity in activities:
                if activity in newPost['activities']:
                    score += 1
            if toLocation == newPost.get('destinationLocation') and score > 0:
                newPost['score'] = round(score * 5 / totalScore, 1)
                newPosts.append(newPost)
        finalPosts = sorted(newPosts, key=lambda x: x['score'], reverse=True)
        return render_template('plan_trip.html', emailId=emailId, name=name, activities=finalPosts)

    else:
        for activity in activities:
            newActivity = vars(activity)
            newActivity['activities'] = json.loads(newActivity.get('activities'))
            newActivity['memberEmails'] = list(set(json.loads(newActivity.get('memberEmails'))))
            del newActivity['_sa_instance_state']
            newActivity['groupSize'] = len(newActivity.get('memberEmails')) + 1
            newActivity['isPrimary'] = newActivity.get('primaryEmail') == emailId
            newActivity['isMember'] = emailId in newActivity['memberEmails']
            newActivity['isNonMember'] = newActivity['isPrimary'] == False and newActivity['isMember'] == False
            newActivity['attachments'] = json.loads(newActivity.get('attachments'))
            newActivity['userMembers'] = newActivity.get('userMembers')

            newAttachments = newActivity.get('attachments')

            message = getInsight(newActivity.get('primaryEmail'), newAttachments)

            newActivity['message'] = message

            newActivities.append(newActivity)

        return render_template('plan_trip.html', name=name, activities=newActivities, emailId=emailId)


@app.route('/join-group', methods=['GET', 'POST'])
def route_join_group():
    postId = request.args.get('postId')
    applierEmailId = request.args.get('emailId')

    post = db.session.query(Posts).filter_by(postId=postId).first()

    newMemberEmails = list(set(json.loads(post.memberEmails)))
    newMemberEmails.append(applierEmailId)

    post.memberEmails = json.dumps(list(set(newMemberEmails)))
    db.session.commit()
    return redirect(request.referrer)


@app.route('/user-activities', methods=['GET', 'POST'])
def route_user_activities():
    emailId = request.args.get('emailId')

    name = db.session.query(Users).filter_by(email=emailId)[0].__dict__.get('name')
    activities = db.session.query(Posts).all()

    newActivities = []

    for activity in activities:
        newActivity = vars(activity)
        newActivity['activities'] = json.loads(newActivity.get('activities'))
        newActivity['memberEmails'] = list(set(json.loads(newActivity.get('memberEmails'))))
        del newActivity['_sa_instance_state']
        newActivity['groupSize'] = len(newActivity.get('memberEmails')) + 1
        newActivity['isPrimary'] = newActivity.get('primaryEmail') == emailId
        newActivity['isMember'] = emailId in newActivity['memberEmails']
        newActivity['isNonMember'] = newActivity['isPrimary'] == False and newActivity['isMember'] == False

        newActivity['attachments'] = json.loads(newActivity.get('attachments'))
        newAttachments = newActivity.get('attachments')
        message = getInsight(newActivity.get('primaryEmail'), newAttachments)
        newActivity['message'] = message

        if newActivity['isPrimary'] or newActivity['isMember']:
            newActivities.append(newActivity)

    return render_template('user_activities.html', name=name, activities=newActivities, emailId=emailId)


@app.route('/post-activity', methods=['GET', 'POST'])
def route_post_activity():
    emailId = request.args.get('emailId')
    personName = db.session.query(Users).filter_by(email=emailId)[0].__dict__.get('name')

    if (request.args.get('tripName') is not None):
        tripName = request.args.get('tripName')
        tripStartDate = request.args.get('tripStartDate')
        tripEndDate = request.args.get('tripEndDate')
        fromLocation = request.args.get('fromLocation')
        toLocation = request.args.get('toLocation')
        activities = json.dumps(request.args.getlist('plannedActivity'))
        vaccinationStatus = request.args.get('userMemberVaccine')
        gender = request.args.get('userMembers')
        ageGroup = request.args.get('userMember')
        userMembers = list()
        userMembers.append((gender,ageGroup, vaccinationStatus))

        db.session.add( Posts( tripName,activities, tripStartDate, tripEndDate, fromLocation, toLocation, emailId, str(userMembers)));
        db.session.commit();

        return render_template('post_activity.html', emailId=emailId, name=personName,
                               successMessage="Activity posted successfully!")

    return render_template('post_activity.html', emailId=emailId, name=personName)


@app.route('/search-activity', methods=['GET', 'POST'])
def route_search_activity():
    emailId = request.args.get('emailId')
    personName = db.session.query(Users).filter_by(email=emailId)[0].__dict__.get('name')

    if (request.args.get('toLocation') is not None):
        tripStartDate = request.args.get('tripStartDate')
        tripEndDate = request.args.get('tripEndDate')
        fromLocation = request.args.get('fromLocation')
        toLocation = request.args.get('toLocation')
        activities = request.args.getlist('plannedActivity')

        posts = db.session.query(Posts).all()

        newPosts = []

        for post in posts:
            newPost = vars(post)
            newPost['activities'] = json.loads(newPost.get('activities'))
            newPost['memberEmails'] = list(set(json.loads(newPost.get('memberEmails'))))
            del newPost['_sa_instance_state']
            newPost['groupSize'] = len(newPost.get('memberEmails')) + 1
            newPost['isPrimary'] = newPost.get('primaryEmail') == emailId
            newPost['isMember'] = emailId in newPost['memberEmails']
            newPost['isNonMember'] = newPost['isPrimary'] == False and newPost['isMember'] == False
            newPost['attachments'] = json.loads(newPost.get('attachments'))

            newAttachments = newPost.get('attachments')

            message = getInsight(newPost.get('primaryEmail'), newAttachments)

            newPost['message'] = message

            totalScore = 8 + 3 + len(newPost['activities']) + 1

            score = getScoreFromaAttachments(newPost.get('primaryEmail'), newAttachments)

            delta = datetime.strptime(tripStartDate, '%Y-%m-%d').date() - datetime.strptime(
                newPost.get('tripStartDate'), '%Y-%m-%d').date()
            if abs(delta.days) <= 15:
                score += 1

            if toLocation == newPost.get('destinationLocation'):
                score += 1

            if fromLocation == newPost.get('fromLocation'):
                score += 1

            if newPost['groupSize'] > 1:
                score += 1

            for activity in activities:
                if activity in newPost['activities']:
                    score += 1
            if toLocation == newPost.get('destinationLocation') and score > 0:
                newPost['score'] = round(score * 5 / totalScore, 1)
                newPosts.append(newPost)
        finalPosts = sorted(newPosts, key=lambda x: x['score'], reverse=True)
        return render_template('search_activity_success.html', emailId=emailId, name=personName, activities=finalPosts)

    return render_template('search_activity.html', emailId=emailId, name=personName)


@app.route('/view-post', methods=['GET', 'POST'])
def route_view_post():
    emailId = request.args.get('emailId')
    personName = db.session.query(Users).filter_by(email=emailId)[0].__dict__.get('name')

    postId = request.args.get('postId')
    post = vars(db.session.query(Posts).filter_by(postId=postId).first())

    post['activities'] = json.loads(post.get('activities'))
    post['memberEmails'] = list(set(json.loads(post.get('memberEmails'))))
    del post['_sa_instance_state']
    post['groupSize'] = len(post.get('memberEmails')) + 1
    post['isPrimary'] = post.get('primaryEmail') == emailId
    post['isMember'] = emailId in post['memberEmails']
    post['isNonMember'] = post['isPrimary'] == False and post['isMember'] == False
    post['attachments'] = json.loads(post.get('attachments'))

    if post['isNonMember']:
        return render_template('view_post.html', emailId=emailId, name=personName, activity={})
    else:
        return render_template('view_post.html', emailId=emailId, name=personName, activity=post)


@app.route('/upload-itinerary', methods=['POST'])
def route_upload_itinerary():
    emailId = request.form.get('emailId')
    postId = request.form.get('postId')

    itineraryType = request.form.get('itineraryType')
    travelAgency = request.form.get('travelAgency')
    ticketNo = request.form.get('ticketNo')
    consentToShare = request.form.get('consent')

    verified = "yes" if travelAgency == 'expedia' else "no"

    file = request.files['file']
    filename = secure_filename(file.filename)
    filePath = os.path.join(app.config['UPLOAD_FOLDER'],
                            filename.split(".")[0] + '_' + emailId + "." + filename.split(".")[1])
    file.save(filePath)

    post = db.session.query(Posts).filter_by(postId=postId).first()

    itineraryAttachments = json.loads(post.attachments)

    if emailId not in itineraryAttachments:
        itineraryAttachments[emailId] = {}

    itineraryAttachments[emailId][itineraryType] = {}
    itineraryAttachments[emailId][itineraryType]['consentToShare'] = consentToShare;
    itineraryAttachments[emailId][itineraryType]['ticketNo'] = ticketNo
    itineraryAttachments[emailId][itineraryType]['travelAgency'] = travelAgency
    itineraryAttachments[emailId][itineraryType]['filePath'] = filePath
    itineraryAttachments[emailId][itineraryType]['verified'] = verified
    print(itineraryAttachments)

    post.attachments = json.dumps(itineraryAttachments)
    db.session.commit()

    return redirect(url_for('route_view_post', emailId=emailId, postId=postId))


def getInsight(primaryEmail, newAttachments):
    isPrimaryCustomerUploaded = False

    if primaryEmail in newAttachments:
        isPrimaryCustomerUploaded = True

    memberUploadedCount = len(newAttachments)

    attachmentTypes = set()
    verifiedCount = 0
    totalTickets = 0
    for memberAttachments in newAttachments.values():
        totalTickets += len(memberAttachments)
        for attachmentType, attachmentDetails in memberAttachments.items():
            attachmentTypes.add(attachmentType)
            if attachmentDetails.get('verified') == 'yes':
                verifiedCount += 1

    message = ""
    if isPrimaryCustomerUploaded and memberUploadedCount == 1:
        message += "Primary member has uploaded the tickets"
    elif isPrimaryCustomerUploaded and memberUploadedCount > 1:
        message += str(memberUploadedCount) + " members along with primary member has uploaded the tickets"
    elif memberUploadedCount != 0:
        message += str(memberUploadedCount) + "member(s) uploaded tickets"

    if message != "":
        message += " for " + ", ".join(attachmentTypes) + ".So " + str(
            verifiedCount) + " tickets are verified by expedia out of " + str(totalTickets) + "."

    return message


def getScoreFromaAttachments(primaryEmail, newAttachments):
    isPrimaryCustomerUploaded = False

    if primaryEmail in newAttachments:
        isPrimaryCustomerUploaded = True

    memberUploadedCount = len(newAttachments)

    attachmentTypes = set()
    verifiedCount = 0
    totalTickets = 0
    for memberAttachments in newAttachments.values():
        totalTickets += len(memberAttachments)
        for attachmentType, attachmentDetails in memberAttachments.items():
            attachmentTypes.add(attachmentType)
            if attachmentDetails.get('verified') == 'yes':
                verifiedCount += 1

    score = 0
    if isPrimaryCustomerUploaded:
        score += 1
        if memberUploadedCount > 1:
            score += 1
    elif memberUploadedCount > 0:
        score += 1
    if totalTickets > 0:
        score += 1
        if verifiedCount > 0:
            score += 1
    score += len(attachmentTypes)
    return score


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

def getInsightFromUserMebers(userMembers ):
    vaccinationCount  = 0
    for gender,ageGroup,vaccinationInd in userMembers:
        if vaccinationInd == 'Yes':
            vaccinationCount += 1
    if  vaccinationCount > 0:
        message1 = str(vaccinationCount) +"members are vaccinated"



@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)


if __name__ == '__main__':
    socketio.run(app,debug=True)
    #socketio.stop()
