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
    recipe_df = recipe_df.fillna("")
    recipe_df['keywords'] = recipe_df['food_name'].astype(str) +recipe_df['season'].astype(str)  +recipe_df['food_type'].astype(str)+recipe_df['crockpot'].astype(str) +recipe_df['source'].astype(str)
    recipe_df['img_source'] = recipe_df['img_source'].apply(lambda x: '<img class="food-img" src={}></img>'.format(x))

    keep_cols = ['keywords','img_source', 'food_name', 'source']
    soup = BeautifulSoup(recipe_df[keep_cols].to_html(index=False, escape=False), "html.parser")
    soup.find('table')['id'] = 'recipe-table'
    rows = soup.find_all('tr')
    rows[0]['class'] = 'header'

    rows[0].find_all('th')[0]['class'] = 'keyword-column'
    for i in range(recipe_df.shape[0]):#enumerate(recipe_df['meal_id']):
        rows[i+1]['id'] = recipe_df['meal_id'].iloc[i]
        rows[i+1].find_all('td')[0]['class'] = 'keyword-column'
        image = soup.new_tag('td')

    #new_tag = soup.new_tag("Your Tag") #add even more tags as needed
    #new_tag.append("Your Text")
    # insert the new tag after the last tag using insert_after
    #the_last_tag_i_want_to_insert_after.insert_after(new_tag)


    dets = "Here are ingredients... Here are instructions..."

    return render_template("recipe-search.html", table=soup, dets=dets)




if __name__ == "__main__":
    app.run(debug=True)
