import os
import numpy as np
from flask import Flask, request, jsonify, render_template, flash
import pickle

app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
model = pickle.load(open('model.p', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():

    year = request.form.get('year')
    weekday = request.form.get('weekday')
    winning_pct = request.form.get('winning_percentage')
    total_games_played = request.form.get("total_games_played")
    pop_opp = request.form.get("pop_opp")

    error = False

    # checking for correct year inputt
    try:
        year = int(year)
    except ValueError:
        flash("Incorrect year. Type in a year from 1994 - 2021", category='error')
        error = True
    
    try:
        weekday = int(weekday)
    except ValueError:
        flash("Incorrect weekday. Enter 1 for weekday game. Enter 0 for weekend game", category='error')
        error = True

    try:
        winning_pct = float(winning_pct)
    except ValueError:
        flash("Incorrect winning percentage, enter winning percentage from 0.00 - 1.00", category='error')
        error = True
    
    try:
        total_games_played = int(total_games_played)
    except ValueError:
        flash("Incorrect # of total games, enter a number from 0 - 162", category='error')
        error = True
    
    try:
        pop_opp = int(pop_opp)
    except ValueError:
        flash("Incorrect popular opponent input. Enter 1 for popular opponent (NYY, BOS, LAD, ANA, SFG), 0 otherwise", category='error')
        error = True

    if error == False:
        if (year > 2021 or year < 1994):
            flash("Incorrect year. Type in a year from 1994 - 2021", category='error')
                
        if (weekday != 1 and weekday != 0):
            flash("Incorrect weekday. Enter 1 for weekday game. Enter 0 for weekend game", category='error')
    
        if (winning_pct > 1 or winning_pct < 0):
            flash("Incorrect winning percentage, enter winning percentage from 0.00 - 1.00", category='error')
    
        if (total_games_played < 0 or total_games_played > 162):
            flash("Incorrect # of total games, enter a number from 0 - 162", category='error')
    
        if (pop_opp != 1 and pop_opp != 0):
            flash("Incorrect popular opponent input. Enter 1 for popular opponent (NYY, BOS, LAD, ANA, SFG), 0 otherwise", category='error')
    
    
        else :
            features = [winning_pct, year, total_games_played, weekday, pop_opp]
            final_features = [np.array(features)]
            print(final_features)
            prediction = model.predict(final_features)
            output = round(prediction[0])
            return render_template('index.html', prediction_text='Total Attendance:{}'.format(output))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)