from flask import Flask, render_template, request, redirect
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
    recipe_df = psql.read_csv('./data/sql_df.csv')
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
    query = "select * from recipe"
    #recipe_df = psql.read_sql(query, con=engine)

    '''
    recipe_df = psql.read_csv('./data/sql_df.csv')
    meal_id = str(recipe_df['meal_id'].astype(int).max() + 1)

    img_source = './static/images/'+meal_id+'.jpg'
    url_for_img = request.form.get('meal-img-url')
    urllib.request.urlretrieve(url_for_img, img_save_fp)
    '''
    food_name = request.form.get('recipe-name')
    meal_type = request.form.getlist('meal-type')
    meal_season = request.form.getlist('meal-season')
    meal_crockpot = request.form.getlist('meal-crockpot')
    meal_src = request.form.get('meal-src-url')
    text_instructions = request.form.get('text-instructions')
    ing_tags = request.form.get('ingredient-tags')
    print(text_instructions)
    print(meal_type)
    return render_template("add-recipe.html", instructions=text_instructions)
    '''

        if request.method == "POST" and form.validate():
            username  = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()

            x = c.execute("SELECT * FROM users WHERE username = (%s)",
                          (thwart(username)))

            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form)

            else:
                c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
                          (thwart(username), thwart(password), thwart(email), thwart("/introduction-to-python-programming/")))

                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('dashboard'))

        return render_template("register.html", form=form)


    except Exception as e:
        return(str(e))
    '''







if __name__ == "__main__":
    app.run(debug=True)
