import pandas as pd
from flask import request
from flask import Flask, render_template

app = Flask(__name__)
dataset = pd.read_csv('./bgg.csv')

def findGames(strategy, thematic, children, party, abstract, war, family, customizable, min_age, min_players, max_time):
    settings = [float(strategy), float(thematic), float(children), float(
        party), float(abstract), float(war), float(family), float(customizable)]

    settedData = dataset.loc[dataset['Strategy'] == settings[0]].loc[dataset['Thematic'] == settings[1]].loc[dataset['Children'] == settings[2]].loc[dataset['Party'] == settings[3]].loc[dataset['Abstract'] == settings[4]].loc[dataset['War'] == settings[5]].loc[dataset['Family'] == settings[6]].loc[dataset['Customizable'] == settings[7]]

    result = settedData.loc[settedData['Min Players'] >= min_players].loc[settedData['Min Age']>= min_age].loc[settedData['Play Time'] <= max_time]
    if result.empty:
        game_advice = 'По вашим параметрам игр не найдено :('
    else:
        resList = result.iloc[0:10, 2:3].values.tolist()
        game_advice = ''
        for i in range(len(resList)):
            game_advice += resList[i][0]
            game_advice += '; '
        game_advice = game_advice[:-2]
    return game_advice

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/found', methods=['GET', 'POST', 'DELETE'])
def get_settings():
    if request.method == "POST":
        strategy = request.form['strategy']
        thematic = request.form['thematic']
        children = request.form['children']
        party = request.form['party']
        abstract = request.form['abstract']
        war = request.form['war']
        family = request.form['family']
        custom = request.form['customize']
        min_players = request.form['min_players']
        min_age = request.form['min_age']
        max_time = request.form['max_time']
        result = findGames(float(strategy), float(thematic), float(children), float(party), float(abstract), float(war), float(family), float(custom),  int(min_age), int(min_players), int(max_time))
        return render_template('result.html', res=result)

if __name__ == '__main__':
    app.run(debug=True)