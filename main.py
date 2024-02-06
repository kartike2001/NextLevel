import hashlib
import random
import string
import bcrypt
from flask import Flask, request, make_response, render_template, redirect, url_for, send_from_directory
from pymongo import MongoClient
import helpers
from flask import jsonify
import csv

app = Flask(__name__)
mongo_client = MongoClient("mongo")
db = mongo_client["next-level"]
userpass = db["userpass"]
usertoken = db["usertoken"]
teampts = db["teampts"]
correct_answers = {
    "Q1": "AMDFH", "Q2": "LNSGE", "Q3": "RMSGT", "Q4": "SZZJK", "Q5": "TMMAR",
    "Q6": "TVSGH", "Q7": "ALPXZ", "Q8": "XMRKM", "Q9": "WHLPS", "Q10": "JSDRJ",
    "Q11": "XWEWY", "Q12": "PYMJT", "Q13": "BWUFL", "Q14": "WPPQB", "Q15": "DHJPK",
    "Q16": {'ZYOGW', 'JETCE', 'YRQOP', 'WSXXE', 'WVDFX', 'EQXMO', 'QGPHM', 'MWWYT', 'ZURAO', 'ZCTEH', 'EUKGB', 'MCJFG',
            'QMKUV', 'YOSSO', 'MYBXZ', 'RMKST', 'TCOOJ', 'UYBIO', 'CBPQH', 'SUPMI', 'UDCUE', 'RPSDO', 'LANMO', 'ZKTNO',
            'TIROT', 'ZBBKW', 'CUBWG', 'OTWMQ', 'GBYKG', 'EYTTN', 'UYDOK', 'LJFOZ', 'MSDGD', 'KEXBH', 'HOMRD', 'LBWKT',
            'BCCOA', 'LJTCZ', 'WIZNB', 'EBJAV', 'KHQTH', 'CVNZY', 'OUKFH', 'MMJLO', 'WLHIG', 'TXSIL', 'PEUGB', 'XVLHA',
            'MIVNT', 'MCSZK'}
}

question_points = {
    "Q1": 10, "Q2": 10, "Q3": 30, "Q4": 10, "Q5": 10,
    "Q6": 10, "Q7": 20, "Q8": 50, "Q9": 50, "Q10": 50,
    "Q11": 20, "Q12": 50, "Q13": 10, "Q14": 10, "Q15": 10,
    "Q16": 10
}


def register_users_from_csv():
    with open('Username.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            username = row['Username']
            password = row['Password']
            if not userpass.find_one({"username": username}):
                password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                userpass.insert_one({"username": username, "password": password_hash})


@app.route('/')
def index():
    allcookies = request.cookies
    response = make_response(render_template('index.html'))
    visits = int(allcookies.get('visits', 0)) + 1
    response.set_cookie('visits', str(visits), max_age=3600)
    return response


@app.route('/game')
def game():
    user = ""
    token = request.cookies.get('token')
    questions_answered_correctly = []
    all_q16_used = False
    if token:
        user_data = usertoken.find_one({"token": token})
        if user_data:
            user = user_data.get("username", "")
            team_data = teampts.find_one({"username": user})
            if team_data:
                questions_answered_correctly = team_data.get("questions", [])
                used_q16_codes = team_data.get("used_q16_codes", [])
                all_q16_used = set(used_q16_codes) == set(correct_answers["Q16"])

    return render_template('game.html', team=user, questions_correct=questions_answered_correctly,
                           all_q16_used=all_q16_used)


@app.route('/leaderboard')
def leaderboard():
    leaderboard_data = teampts.find().sort("points", -1)
    leaderboard_list = [(entry.get("username"), entry.get("points", 0)) for entry in leaderboard_data]

    response = make_response(render_template('leaderboard.html', leaderboard=leaderboard_list))
    visits = int(request.cookies.get('visits', 0)) + 1
    response.set_cookie('visits', str(visits), max_age=3600)
    return response


@app.route('/leaderboard_data')
def leaderboard_data():
    sorted_data = teampts.find().sort("points", -1)
    leaderboard_data = [{"username": entry.get("username"), "points": entry.get("points", 0)} for entry in sorted_data]
    return jsonify(leaderboard_data)


@app.route('/mentors')
def mentors():
    allcookies = request.cookies
    response = make_response(render_template('mentors.html'))
    visits = int(allcookies.get('visits', 0)) + 1
    response.set_cookie('visits', str(visits), max_age=3600)
    return response


@app.route('/login')
def login():
    allcookies = request.cookies
    response = make_response(render_template('login.html'))
    visits = int(allcookies.get('visits', 0)) + 1
    response.set_cookie('visits', str(visits), max_age=3600)
    return response


@app.route('/registeruser', methods=['POST'])
def register_user():
    username = request.form.get('username')
    password = request.form.get('regpass')
    if not helpers.is_valid_input(username) or not helpers.is_valid_input(password):
        return "Invalid input", 400

    if userpass.find_one({"username": username}):
        return "Username already exists", 400

    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    userpass.insert_one({"username": username, "password": password_hash})
    return redirect(url_for('login'))


@app.route('/loginuser', methods=['POST'])
def login_user():
    username = request.form.get('usernamel')
    password = request.form.get('regpassl')

    if not helpers.is_valid_input(username) or not helpers.is_valid_input(password):
        return "Invalid input", 400

    user = userpass.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode(), user["password"]):
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=200))
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        usertoken.insert_one({"username": username, "token": token_hash})
        response = make_response(redirect(url_for('game')))
        response.set_cookie('token', token_hash, max_age=3600)
        return response
    else:
        return "Username not found or password is incorrect", 400


@app.route('/submit', methods=['POST'])
def submit():
    token = request.cookies.get('token')
    if not token:
        return "No token provided", 403

    user_data = usertoken.find_one({"token": token})
    if not user_data:
        return "User not authenticated", 403

    username = user_data["username"]
    team_data = teampts.find_one({"username": username})
    team_used_q16_codes = team_data.get("used_q16_codes", []) if team_data else []
    all_used_q16_codes = [code for team in teampts.find() for code in team.get("used_q16_codes", [])]

    questions_correct = []
    total_points = 0  # Initialize total points to 0

    for q, answer in correct_answers.items():
        user_answer = request.form.get(q)
        if q == "Q16":
            if user_answer in answer and user_answer not in all_used_q16_codes:
                team_used_q16_codes.append(user_answer)
                all_used_q16_codes.append(user_answer)
                teampts.update_one({"username": username}, {"$set": {"used_q16_codes": team_used_q16_codes}},
                                   upsert=True)
                questions_correct.append(q)
                total_points += question_points[q]
        elif user_answer == answer:
            questions_correct.append(q)
            total_points += question_points[q]

    if questions_correct:
        teampts.update_one(
            {"username": username},
            {
                "$push": {"questions": {"$each": questions_correct}},
                "$inc": {"points": total_points}
            },
            upsert=True
        )
    return redirect(url_for('leaderboard'))


@app.route('/assets/img/mentors/<filename>')
def mentor_image(filename):
    return send_from_directory('static/img/mentors', filename)


@app.route('/assets/img/others/<filename>')
def other_image(filename):
    return send_from_directory('static/img/others', filename)


register_users_from_csv()
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
