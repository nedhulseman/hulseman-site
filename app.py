from flask import Flask, render_template
import os


cwd = os.getcwd()

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coffee.db'
#app.secret_key = 'java'
#db = SQLAlchemy(app)

@app.route('/')
def main():
    return render_template("index.html")


@app.route('/Scraping-mlb-headshots-with-beautifulsoup')
def mlb_headshots():
    return render_template("mlb-head.html")

@app.route('/boarding-sim')
def boarding_sim():
    return render_template("boarding-sim.html")

@app.route('/xgboost-allstate')
def xgboost_allstate():
    return render_template("xgboost-allstate.html")


if __name__ == "__main__":
    app.run(debug=True)
