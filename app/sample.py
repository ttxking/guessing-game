from flask import Flask, request, jsonify, render_template, redirect
from pymongo import MongoClient
import os, json, redis

# App
application = Flask(__name__)

# connect to MongoDB
mongoClient = MongoClient('mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_AUTHDB'])
db = mongoClient[os.environ['MONGODB_DATABASE']]

# connect to Redis
redisClient = redis.Redis(host=os.environ.get("REDIS_HOST", "localhost"), port=os.environ.get("REDIS_PORT", 6379), db=os.environ.get("REDIS_DB", 0))

@application.route('/', methods=["GET", "POST"])
def start():
    if request.method == 'POST':

        myInsert = {
            "question" : {
                "first_letter": "_",
                "second_letter": "_",
                "third_letter": "_",
                "fourth_letter": "_"
            },
            "count" : 0,
            "answer" : {
                "first_answer": "_",
                "second_answer": "_",
                "third_answer": "_",
                "fourth_answer": "_"
            },
            "status" : "",
            "restart": False
        }

        db.game.insert_one(myInsert)
        current_game = db.game.find_one()
        return render_template('guessing_game/question.html', current_game=current_game)


    elif request.method == 'GET':
        return render_template('guessing_game/index.html')

       
@application.route('/set_question', methods=["GET", "POST"])
def set_question():
    current_game = db.game.find_one()
    if request.method == 'POST':
        game = db.game.find()
        for ele in game:
            if ele['question']['first_letter'] == "_":
                field = "question.first_letter"
            elif ele['question']['second_letter'] == "_":
                field = "question.second_letter"
            elif ele['question']['third_letter'] == "_":
                field = "question.third_letter"
            elif ele['question']['fourth_letter'] == "_":
                field = "question.fourth_letter"
            else:  
                return redirect ('game')

        if request.form['submit_button'] == "A":
            updated_question = {"$set": {field: 'A'}}
        elif request.form['submit_button'] == "B":
            updated_question = {"$set": {field: 'B'}}
        elif request.form['submit_button'] == "C":
            updated_question = {"$set": {field: 'C'}}
        else:
            updated_question = {"$set": {field: 'D'}}

        db.game.update({}, updated_question)
        return redirect("/set_question")

    elif request.method == 'GET':
        return render_template('guessing_game/question.html', current_game=current_game)

@application.route('/game', methods=["GET", "POST"])
def game():
    current_game = db.game.find_one()
    if request.method == 'POST':
        game = db.game.find()
        for ele in game:
            first_letter = ele['question']['first_letter']
            second_letter = ele['question']['second_letter']
            third_letter = ele['question']['third_letter']
            fourth_letter = ele['question']['fourth_letter']

            if ele['answer']['first_answer'] != first_letter :
                while request.form['submit_button'] != first_letter:
                    db.game.update({}, {"$inc": {"count": 1}})
                    return redirect('/game')
                db.game.update({}, {"$set": {"answer.first_answer": first_letter }})
                return redirect('/game')
                

            elif ele['answer']['second_answer'] != second_letter :
                while request.form['submit_button'] != second_letter:
                    db.game.update({}, {"$inc": {"count": 1}})
                    return redirect('/game')
                db.game.update({}, {"$set": {"answer.second_answer": second_letter }})
                return redirect('/game')

            elif ele['answer']['third_answer'] != third_letter :
                while request.form['submit_button'] != third_letter:
                    db.game.update({}, {"$inc": {"count": 1}})
                    return redirect('/game')
                db.game.update({}, {"$set": {"answer.third_answer": third_letter }})
                return redirect('/game')

            elif ele['answer']['fourth_answer'] != fourth_letter :
                while request.form['submit_button'] != fourth_letter:
                    db.game.update({}, {"$inc": {"count": 1}})
                    return redirect('/game')
                db.game.update({}, {"$set": {"answer.fourth_answer": fourth_letter }})
                db.game.update({}, {"$set": {"status": "You Win !!"}})
                db.game.update({}, {"$set": {"restart": True}})
                return redirect('/game')

    


    elif request.method == 'GET':
        return render_template('guessing_game/game.html', current_game=current_game)

@application.route('/reset', methods=["POST"])
def restart():
    myInsert = {
            "question" : {
                "first_letter": "_",
                "second_letter": "_",
                "third_letter": "_",
                "fourth_letter": "_"
            },
            "count" : 0,
            "answer" : {
                "first_answer": "_",
                "second_answer": "_",
                "third_answer": "_",
                "fourth_answer": "_"
            },
            "status" : "",
            "restart": False
    }
    if request.method == 'POST':
        if request.form['submit_button'] == 'restart':
            db.game.update({}, {"$set": myInsert})
    return redirect('/set_question')

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("FLASK_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("FLASK_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)