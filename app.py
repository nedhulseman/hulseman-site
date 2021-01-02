from flask import Flask, render_template, request, redirect, url_for
from wtforms import Form, BooleanField, TextField, PasswordField, validators
import os
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import pandas.io.sql as psql
#import sqlalchemy

cwd = os.getcwd()
#pw = open("./configs/hulseman_site_config.txt", "r").read().strip()
#engine = sqlalchemy.create_engine('mysql+mysqlconnector://root:'+pw+'@localhost:3306/recipes', echo=True)
query = "select * from recipe"
#recipe_df = psql.read_sql(query, con=engine)
recipe_df = pd.read_csv('./data/sql_df.csv')


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coffee.db'
#app.secret_key = 'java'
#db = SQLAlchemy(app)

@app.route('/')
def main():
    return render_template("index.html")


@app.route('/add-recipe')
def add_recipe():
    return render_template("add-recipe.html")


@app.route('/search-recipes')
def recipe_search():
    query = "select * from recipe"
    #recipe_df = psql.read_sql(query, con=engine)
    #recipe_df = pd.read_excel('data/recipe_list.xlsx', sheet_name='Cookbook')
    recipe_df = pd.read_csv('./data/sql_df.csv')
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



@app.route('/registerRecipe/', methods=["POST", "GET"])
def register_recipe():
    if request.method == "POST":
        query = "select * from recipe"
        #recipe_df = psql.read_sql(query, con=engine)
        recipe_df = pd.read_csv('./data/recipe.csv')
        query = "select * from ingredients"
        #ingredients_df = psql.read_sql(query, con=engine)
        ingredients_df = pd.read_csv('./data/ingredients.csv')


        query = "select * from recipe_ingredients"
        #recipe_ingredients_df = psql.read_sql(query, con=engine)
        recipe_ingredients_df = pd.read_csv('./data/recipe_ingredients.csv')

        meal_id = str(recipe_df['meal_id'].astype(int).max() + 1)

        img_source = './static/images/'+meal_id+'.jpg'
        url_for_img = request.form.get('meal-img-url')
        urllib.request.urlretrieve(url_for_img, img_source)

        food_name = request.form.get('recipe-name')
        meal_type = request.form.getlist('meal-type')
        meal_season = request.form.getlist('meal-season')
        meal_crockpot = request.form.getlist('meal-crockpot')
        if len(meal_crockpot) > 1:
            meal_crockpot = 'both'
        #meal_src = request.form.get('meal-src-url')
        text_instructions = request.form.get('text-instructions')
        ing_tags = request.form.get('ingredient-tags')
        new_row = {
            'meal_id' : [meal_id],
            'food_name': [food_name],
            'season': [','.join(meal_season).lower()],
            'food_type': [','.join(meal_type).lower()],
            'crockpot': [','.join(meal_crockpot).lower()],
            'source': [''],
            'source_type': [''],
            'img_source': [img_source],
            'ingredients': [''],
            'directions': [text_instructions]
        }
        new_meal_df = pd.DataFrame(new_row)


        ingredients_form = pd.DataFrame(columns=['ingredient_id', 'ingredient_name', 'ingredient_amount', 'ingredient_amount_denomination', 'meal_id'])
        new_ingredients = pd.DataFrame()
        for ing in ing_tags.split(','):
            denomination = request.form.get("ing-amt-type-"+ing)
            print(denomination)
            amt = request.form.get("ing-amt-"+ing)
            if ing not in ingredients_df['ingredient_name'].unique():
                ingredient_new_id = str(ingredients_df['ingredient_id'].astype(int).max() + 1)
                row = {'ingredient_name':ing.lower(), 'ingredient_id':ingredient_new_id}
                ingredients_df = ingredients_df.append(row, ignore_index=True)
                new_ingredients = new_ingredients.append(row, ignore_index=True)
            row = {
                'ingredient_id'     : ingredients_df.loc[ingredients_df['ingredient_name']== ing.lower(), 'ingredient_id'].iloc[0],
                'ingredient_name'   : ing.lower(),
                'ingredient_amount' : amt.lower(),
                'ingredient_amount_denomination': denomination,
                'meal_id'           : meal_id
            }
            ingredients_form = ingredients_form.append(row, ignore_index=True)

        #ingredients_form.to_sql('recipe_ingredients', con=engine, if_exists='append')
        #new_ingredients.to_sql('ingredients', con=engine, if_exists='append')
        #new_meal_df.to_sql('recipe', con=engine, if_exists='append')

        ingredients_form.to_csv('./data/recipe_ingredients2.csv',index=False)
        new_meal_df.to_csv('./data/recipe2.csv', index=False)
        new_ingredients.to_csv('./data/ingredients2.csv', index=False)


        return redirect(url_for('recipe_search'))




if __name__ == "__main__":
    app.run(debug=True)
