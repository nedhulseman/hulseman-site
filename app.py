from flask import Flask, render_template, request, redirect, url_for

from wtforms import Form, BooleanField, TextField, PasswordField, validators
import os
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import pandas.io.sql as psql
import sqlalchemy
from sqlalchemy.types import INTEGER, TEXT
import sys
#sys.stdout = open('stdout_python.log', 'a')


cwd = os.getcwd()
#pw = open("./configs/hulseman_site_config.txt", "r").read().strip()
engine = sqlalchemy.create_engine('mysql+mysqlconnector://root:dustPed15@localhost:3306/recipes', echo=True)
query = "select * from recipe"
#recipe_df = pd.read_csv('./data/sql_df.csv')
print('engine created...')
recipe_df_types = {
    'meal_id'     : INTEGER,
    'food_name'   : TEXT,
    'season'      : TEXT,
    'food_type'   : TEXT,
    'crockpot'    : TEXT,
    'source'      : TEXT,
    'source_type' : TEXT,
    'img_source'  : TEXT,
    'img_source'  : TEXT,
    'directions'  : TEXT
}
ingredients_df_types = {
    'ingredient_id'                  : INTEGER,
    'ingredient_name'                : TEXT,
}
recipe_ingredients_df_types = {
    'ingredient_id'                  : INTEGER,
    'ingredient_name'                : TEXT,
    'ingredient_amount_denomination' : TEXT,
    'meal_id'                        : INTEGER,
}


app = Flask(__name__)

app.config['img_dir'] = 'static/images'

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
    recipe_df = psql.read_sql(query, con=engine)
    #recipe_df = pd.read_csv('./data/recipe.csv', engine='python')
    recipe_df['meal_id'] = recipe_df['meal_id'].astype(str)
    recipe_df['directions'] = recipe_df['directions'].apply(lambda x: "<br />".join(x.split("\n")))

    query = "select * from recipe_ingredients"
    recipe_ingredients_df = psql.read_sql(query, con=engine)
    #recipe_ingredients_df = pd.read_csv('./data/recipe_ingredients.csv')
    recipe_ingredients_df['meal_id'] = recipe_ingredients_df['meal_id'].astype(str)
    recipe_ingredients_df['full_amt'] = recipe_ingredients_df['ingredient_amount'].astype(str) +' '+ recipe_ingredients_df['ingredient_amount_denomination'] +' of '+ recipe_ingredients_df['ingredient_name']
    recipe_ingredients_df['full_ingredients'] = recipe_ingredients_df.groupby(['meal_id'])['full_amt'].transform(lambda x : '<br>'.join(x))
    ingredients_str = recipe_ingredients_df[['meal_id', 'full_ingredients']].drop_duplicates()
    recipe_df = pd.merge(recipe_df, ingredients_str, how='left', on='meal_id')
    recipe_df['details'] = '<strong>Ingredients</strong><br>'+recipe_df['full_ingredients'] + '<br><br><strong>Directions</strong><br>'+ recipe_df['directions']
    recipe_df = recipe_df.fillna("")
    recipe_df['keywords'] = recipe_df['food_name'].astype(str) +recipe_df['season'].astype(str)  +recipe_df['food_type'].astype(str)+recipe_df['crockpot'].astype(str) +recipe_df['source'].astype(str)
    recipe_df['img_source'] = recipe_df['img_source'].apply(lambda x: '<img class="food-img" src={}></img>'.format(x))

    keep_cols = ['keywords', 'details', 'img_source', 'food_name', 'source']
    recipe_df_formatted =  recipe_df[keep_cols].rename(columns={'img_source':' ', 'food_name':'Recipe', 'source':'Submitter'})
    soup = BeautifulSoup(recipe_df_formatted.to_html(index=False, escape=False), "html.parser")
    soup.find('table')['id'] = 'recipe-table'
    rows = soup.find_all('tr')
    rows[0]['class'] = 'header'

    rows[0].find_all('th')[0]['class'] = 'keyword-column'
    rows[0].find_all('th')[1]['class'] = 'details-column'
    for i in range(recipe_df.shape[0]):
        rows[i+1]['id'] = recipe_df['meal_id'].iloc[i]
        rows[i+1].find_all('td')[0]['class'] = 'keyword-column'
        rows[i+1].find_all('td')[1]['class'] = 'details-column'
        image = soup.new_tag('td')

    return render_template("recipe-search.html", table=soup)



@app.route('/registerRecipe/', methods=["POST", "GET"])
def register_recipe():
    print('RegisterRecipe is engaged...')
    if request.method == "POST":
        print('RegisterRecipe handling post...')
        query = "select * from recipe"
        recipe_df = psql.read_sql(query, con=engine)
        #recipe_df = pd.read_csv('./data/recipe.csv', engine='python')

        query = "select * from ingredients"
        ingredients_df = psql.read_sql(query, con=engine)
        #ingredients_df = pd.read_csv('./data/ingredients.csv')

        query = "select * from recipe_ingredients"
        recipe_ingredients_df = psql.read_sql(query, con=engine)
        #recipe_ingredients_df = pd.read_csv('./data/recipe_ingredients.csv')

        meal_id = str(recipe_df['meal_id'].astype(int).max() + 1)
        print('meal_id: ' + str(meal_id))

        img = request.files.get("file")
        #filename = upload.filename.rsplit("/")[0]
        #destination = "/".join([target, filename])

        img_source = './static/images/'+meal_id+'.jpg'
        print('\n----')
        print("Accept incoming file:", img.filename)
        print("Save it to:", img_source)
        print('----')
        img.save(os.path.join(app.root_path, 'static/images', meal_id +'.jpg'))
        '''
        url_for_img = request.form.get('meal-img-url')
        if url_for_img.lower() == 'placeholder':
            img_source = './static/images/placeholder.jpg'
        else:
            urllib.request.urlretrieve(url_for_img, img_source)
        '''
        food_name = request.form.get('recipe-name')
        meal_type = request.form.getlist('meal-type')
        meal_season = request.form.getlist('meal-season')
        meal_crockpot = request.form.getlist('meal-crockpot')
        if 'yes' in ", ".join(meal_crockpot).lower():
            meal_crockpot = 'crockpot'
        else:
            meal_crockpot = 'no'
        #meal_src = request.form.get('meal-src-url')
        text_instructions = request.form.get('text-instructions')
        print('\n\n\n-------')
        print(text_instructions)
        ing_tags = request.form.get('ingredient-tags')
        source = request.form.get('submitter-source')
        cook_time = request.form.get('cooktime')
        cook_time_denom = request.form.get('cooktime-drpdwn-btn')
        print(ing_tags)
        print(source)
        new_row = {
            'meal_id' : [meal_id],
            'food_name': [food_name],
            'season': [','.join(meal_season).lower()],
            'food_type': [','.join(meal_type).lower()],
            'crockpot': [','.join(meal_crockpot).lower()],
            'source': [source],
            'source_type': [''],
            'img_source': [img_source],
            #'ingredients': [''],
            'directions': [text_instructions],
            'cook_time': [cook_time],
            'cook_time_denom': [cook_time_denom]
        }
        new_meal_df = pd.DataFrame(new_row)
        print('new meal df')
        print(new_meal_df)

        ingredients_form = pd.DataFrame(columns=['ingredient_id', 'ingredient_name', 'ingredient_amount', 'ingredient_amount_denomination', 'meal_id'])
        new_ingredients = pd.DataFrame()
        for ing in ing_tags.split(','):
            denomination = request.form.get("ing-amt-type-"+ing)
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

        ingredients_form.to_sql('recipe_ingredients', con=engine, dtype=recipe_ingredients_df_types,  if_exists='append', index=False)
        new_ingredients.to_sql('ingredients', con=engine, dtype=ingredients_df_types, if_exists='append', index=False)
        new_meal_df.to_sql('recipe', con=engine, dtype=recipe_df_types, if_exists='append', index=False)
        print(recipe_df)
        print(new_meal_df)
        #recipe_ingredients_df.append(ingredients_form, ignore_index=True).to_csv('./data/recipe_ingredients.csv',index=False)
        #recipe_df.append(new_meal_df, ignore_index=True).to_csv('./data/recipe.csv', index=False)
        #ingredients_df.to_csv('./data/ingredients.csv', index=False)

        print('made it through')

        return redirect(url_for('recipe_search'))




if __name__ == "__main__":
    app.run(debug=True)
