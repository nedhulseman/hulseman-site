from flask import Flask, render_template
import os
import pandas as pd
from bs4 import BeautifulSoup


cwd = os.getcwd()

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coffee.db'
#app.secret_key = 'java'
#db = SQLAlchemy(app)

@app.route('/')
def main():
    return render_template("index.html")


@app.route('/search-recipes')
def recipe_search():
    recipe_df = pd.read_excel('data/recipe_list.xlsx', sheet_name='Cookbook')
    '''
    recipe_df = pd.DataFrame({
        'Name': ['Alfreds Futterkiste', 'Ian An', 'Al Maddock'],
        'Country': ['Germany', 'Sweden', 'UK']
    })
    '''
    soup = BeautifulSoup(recipe_df.to_html(index=False), "html.parser")
    soup.find('table')['id'] = 'recipe-table'
    soup.find('tr')['class'] = 'header'

    dets = "Here are ingredients... Here are instructions..."

    return render_template("recipe-search.html", table=soup, dets=dets)

@app.route('/get-ins')
def get_ins():
    return 'Here are ingredients...\nHere are instructions...'

@app.route('/boarding-sim')
def boarding_sim():
    return render_template("boarding-sim.html")

@app.route('/xgboost-allstate')
def xgboost_allstate():
    return render_template("xgboost-allstate.html")


if __name__ == "__main__":
    app.run(debug=True)
