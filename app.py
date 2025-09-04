# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)




# Database setup
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

init_db()






db = SQLAlchemy(app)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text)
    prep_time = db.Column(db.String(50))
    calories = db.Column(db.String(50))
    category = db.Column(db.String(50))
    image = db.Column(db.String(200))
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'ingredients': self.ingredients.split(','),
            'steps': self.steps.split('|') if self.steps else [],
            'prep_time': self.prep_time,
            'calories': self.calories,
            'category': self.category,
            'image': self.image
        }

def initialize_database():
    with app.app_context():
        db.create_all()
        if Recipe.query.count() == 0:
            sample_recipes = [
                Recipe(
                    title="Butter Chicken",
                    ingredients="Chicken,Butter,Tomatoes,Cream,Spices",
                    steps="Marinate chicken|Cook gravy with tomatoes and spices|Add butter and cream|Combine and simmer",
                    prep_time="45 mins",
                    calories="350 kcal",
                    category="dinner",
                    image="/static/images/butter-chicken-3.jpg"
                ),
                Recipe(
                    title="Palak Paneer",
                    ingredients="Spinach,Paneer,Garlic,Onion,Spices",
                    steps="Blanch and blend spinach|Saute onion and spices|Add paneer and spinach puree",
                    prep_time="35 mins",
                    calories="280 kcal",
                    category="dinner",
                    image="/static/images/palak-paneer.jpg"
                ),
                Recipe(
                    title="Hyderabadi Biryani",
                    ingredients="Rice,Chicken/Mutton,Yogurt,Spices,Onions",
                    steps="Marinate meat|Cook partially rice|Layer rice and meat|Cook on low heat",
                    prep_time="1 hr",
                    calories="420 kcal",
                    category="dinner",
                    image="/static/images/biriyani.jpg"
                ),
                Recipe(
                    title="Chole Bhature",
                    ingredients="Chickpeas,Flour,Yogurt,Tomatoes,Spices",
                    steps="Soak and boil chickpeas|Prepare spicy tomato gravy|Knead dough and make bhature|Serve hot",
                    prep_time="50 mins",
                    calories="500 kcal",
                    category="lunch",
                    image="/static/images/Chole Bhature.jpg"
                ),
                Recipe(
                    title="Masala Dosa",
                    ingredients="Rice,Lentils,Potatoes,Mustard seeds,Curry leaves",
                    steps="Make dosa batter|Prepare potato filling|Cook dosa and stuff with filling",
                    prep_time="40 mins",
                    calories="300 kcal",
                    category="breakfast",
                    image="/static/images/Masala-Dosa.webp"
                ),
                Recipe(
                    title="Rajma Chawal",
                    ingredients="Kidney beans,Rice,Tomatoes,Onions,Spices",
                    steps="Soak and cook rajma|Prepare tomato-onion gravy|Serve hot with rice",
                    prep_time="45 mins",
                    calories="330 kcal",
                    category="lunch",
                    image="/static/images/Rajma Chawal.webp"
                ),
                Recipe(
                    title="Aloo Paratha",
                    ingredients="Potatoes,Wheat flour,Spices,Butter,Green chilies",
                    steps="Boil and mash potatoes|Mix with spices|Stuff into dough and roll|Cook on tawa with butter",
                    prep_time="30 mins",
                    calories="290 kcal",
                    category="breakfast",
                    image="/static/images/Aloo Paratha.jpg"
                ),
                Recipe(
                    title="Paneer Tikka",
                    ingredients="Paneer,Yogurt,Spices,Capsicum,Onion",
                    steps="Marinate paneer and veggies|Skewer and grill or bake|Serve with chutney",
                    prep_time="25 mins",
                    calories="270 kcal",
                    category="appetizer",
                    image="/static/images/Paneer-Tikka.webp"
                ),
                Recipe(
                    title="Dhokla",
                    ingredients="Gram flour,Yogurt,Eno,Mustard seeds,Curry leaves",
                    steps="Make batter with gram flour and yogurt|Add eno and steam|Prepare tempering and pour over dhokla",
                    prep_time="20 mins",
                    calories="180 kcal",
                    category="snack",
                    image="/static/images/Dhokla.webp"
                ),
                Recipe(
                    title="Gulab Jamun",
                    ingredients="Khoya,Flour,Sugar,Cardamom,Rose water",
                    steps="Make dough with khoya and flour|Shape balls and fry|Dip in sugar syrup",
                    prep_time="30 mins",
                    calories="350 kcal",
                    category="dessert",
                    image="/static/images/Gulab Jamun.jpeg"
                ),
                # Chinese Recipes
                Recipe(
                    title="Kung Pao Chicken",
                    ingredients="Chicken,Peanuts,Chili peppers,Garlic,Soy sauce",
                    steps="Marinate chicken|Stir-fry chilies and garlic|Add chicken and sauce|Garnish with peanuts",
                    prep_time="40 mins",
                    calories="390 kcal",
                    category="chinese",
                    image="/static/images/Kung-Pao-Chicken.webp"
                ),
                Recipe(
                    title="Sweet and Sour Pork",
                    ingredients="Pork,Pineapple,Bell peppers,Vinegar,Sugar",
                    steps="Fry pork cubes|Cook sauce with vinegar and sugar|Combine with pork and vegetables",
                    prep_time="35 mins",
                    calories="420 kcal",
                    category="chinese",
                    image="/static/images/Sweet and Sour Pork.jpg"
                ),
                Recipe(
                    title="Fried Rice",
                    ingredients="Rice,Eggs,Vegetables,Soy sauce,Green onions",
                    steps="Scramble eggs|Stir-fry veggies|Add rice and soy sauce|Mix with green onions",
                    prep_time="30 mins",
                    calories="330 kcal",
                    category="chinese",
                    image="/static/images/Fried Rice.jpg"
                ),
                Recipe(
                    title="Spring Rolls",
                    ingredients="Spring roll wrappers,Cabbage,Carrots,Soy sauce,Garlic",
                    steps="Prepare filling|Wrap in spring roll sheets|Deep fry until golden",
                    prep_time="25 mins",
                    calories="250 kcal",
                    category="chinese",
                    image="/static/images/Spring Rolls.jpg"
                ),
                Recipe(
                    title="Beef and Broccoli",
                    ingredients="Beef,Broccoli,Oyster sauce,Garlic,Cornstarch",
                    steps="Marinate beef|Blanch broccoli|Stir-fry with sauce",
                    prep_time="35 mins",
                    calories="380 kcal",
                    category="chinese",
                    image="/static/images/Beef and Broccoli.jpg"
                ),

                # Italian Recipes
                Recipe(
                    title="Spaghetti Carbonara",
                    ingredients="Spaghetti,Eggs,Pancetta,Parmesan cheese,Black pepper",
                    steps="Boil pasta|Cook pancetta|Mix eggs and cheese|Combine all with pasta",
                    prep_time="30 mins",
                    calories="400 kcal",
                    category="italian",
                    image="/static/images/Spaghetti-Carbonara.jpg"
                ),
                Recipe(
                    title="Margherita Pizza",
                    ingredients="Pizza dough,Tomato sauce,Mozzarella,Basil,Olive oil",
                    steps="Prepare dough|Spread sauce and toppings|Bake in oven",
                    prep_time="40 mins",
                    calories="350 kcal",
                    category="italian",
                    image="/static/images/Margherita-Pizza.jpg"
                ),
                Recipe(
                    title="Lasagna",
                    ingredients="Lasagna noodles,Ground beef,Tomato sauce,Ricotta,Mozzarella",
                    steps="Cook meat|Layer pasta with sauce and cheese|Bake in oven",
                    prep_time="1 hr",
                    calories="500 kcal",
                    category="italian",
                    image="/static/images/Lasagna.jpg"
                ),
                Recipe(
                    title="Risotto alla Milanese",
                    ingredients="Arborio rice,Saffron,Onion,Butter,Parmesan",
                    steps="Saute onions|Add rice and broth gradually|Stir in saffron and cheese",
                    prep_time="45 mins",
                    calories="380 kcal",
                    category="italian",
                    image="/static/images/Risotto-alla-Milanese.jpg"
                ),
                Recipe(
                    title="Tiramisu",
                    ingredients="Ladyfingers,Mascarpone,Coffee,Cocoa powder,Eggs",
                    steps="Dip ladyfingers in coffee|Layer with mascarpone mixture|Chill and dust with cocoa",
                    prep_time="25 mins",
                    calories="420 kcal",
                    category="italian",
                    image="/static/images/Tiramisu.jpg"
                ),
                Recipe(
                    title="Fettuccine Alfredo",
                    ingredients="Fettuccine,Butter,Parmesan,Cream,Garlic",
                    steps="Cook pasta|Prepare creamy garlic sauce|Mix with pasta",
                    prep_time="30 mins",
                    calories="390 kcal",
                    category="italian",
                    image="/static/images/Fettuccine-Alfredo.jpg"
                ),
                Recipe(
                    title="Caprese Salad",
                    ingredients="Tomatoes,Mozzarella,Basil,Olive oil,Salt",
                    steps="Slice tomatoes and cheese|Arrange and top with basil and oil",
                    prep_time="15 mins",
                    calories="220 kcal",
                    category="italian",
                    image="/static/images/Caprese-Salad.jpg"
                ),
                Recipe(
                    title="Gnocchi",
                    ingredients="Potatoes,Flour,Eggs,Salt,Parmesan",
                    steps="Boil and mash potatoes|Form dough|Shape gnocchi and boil",
                    prep_time="50 mins",
                    calories="340 kcal",
                    category="italian",
                    image="/static/images/Gnocchi.jpg"
                ),
                Recipe(
                    title="Bruschetta",
                    ingredients="Bread,Tomatoes,Garlic,Basil,Olive oil",
                    steps="Toast bread|Top with tomato mix|Drizzle olive oil",
                    prep_time="20 mins",
                    calories="180 kcal",
                    category="italian",
                    image="/static/images/Bruschetta.webp"
                ),
                Recipe(
                    title="Panna Cotta",
                    ingredients="Cream,Sugar,Vanilla,Gelatin,Berries",
                    steps="Heat cream and vanilla|Add gelatin and chill|Serve with berries",
                    prep_time="25 mins",
                    calories="300 kcal",
                    category="italian",
                    image="/static/images/Panna-Cotta.jpg"
                ),

                # Mexican Recipes
                Recipe(
                    title="Tacos Al Pastor",
                    ingredients="Pork shoulder,Pineapple,Corn tortillas,Onion,Cilantro",
                    steps="Marinate pork|Grill and slice meat|Warm tortillas|Assemble with toppings",
                    prep_time="45 mins",
                    calories="450 kcal",
                    category="mexican",
                    image="/static/images/takos-al-pastor.jpg"
                ),
                Recipe(
                    title="Chicken Enchiladas",
                    ingredients="Shredded chicken,Tortillas,Enchilada sauce,Cheese,Onions",
                    steps="Fill tortillas with chicken|Cover with sauce and cheese|Bake until melted",
                    prep_time="40 mins",
                    calories="500 kcal",
                    category="mexican",
                    image="/static/images/Chicken-Enchiladas.jpg"
                ),
                Recipe(
                    title="Guacamole",
                    ingredients="Avocados,Lime,Tomato,Onion,Cilantro",
                    steps="Mash avocados|Mix in other ingredients|Season to taste",
                    prep_time="10 mins",
                    calories="200 kcal",
                    category="mexican",
                    image="/static/images/Guacamole.jpg"
                ),
                Recipe(
                    title="Chiles Rellenos",
                    ingredients="Poblano peppers,Cheese,Eggs,Tomato sauce,Flour",
                    steps="Roast and peel peppers|Stuff with cheese|Dip in egg batter and fry",
                    prep_time="1 hr",
                    calories="600 kcal",
                    category="mexican",
                    image="/static/images/chile-rellenos.jpg"
                ),
                Recipe(
                    title="Mexican Rice",
                    ingredients="Rice,Tomato paste,Garlic,Onion,Chicken broth",
                    steps="Sauté rice and vegetables|Add tomato paste and broth|Simmer until cooked",
                    prep_time="30 mins",
                    calories="300 kcal",
                    category="mexican",
                    image="/static/images/Mexican-Rice.jpg"
                ),

                # Indian Recipes
                Recipe(
                    title="Palak Paneer",
                    ingredients="Spinach,Paneer,Garlic,Onion,Spices",
                    steps="Blanch and blend spinach|Saute onion and spices|Add paneer and spinach puree",
                    prep_time="35 mins",
                    calories="280 kcal",
                    category="indian",
                    image="/static/images/palak-paneer.jpg"
                ),
                Recipe(
                    title="Rajma Chawal",
                    ingredients="Kidney beans,Rice,Tomatoes,Onions,Spices",
                    steps="Soak and cook rajma|Prepare tomato-onion gravy|Serve hot with rice",
                    prep_time="45 mins",
                    calories="330 kcal",
                    category="indian",
                    image="/static/images/Rajma-Chawal.webp"
                ),
                Recipe(
                    title="Paneer Tikka",
                    ingredients="Paneer,Yogurt,Spices,Capsicum,Onion",
                    steps="Marinate paneer and veggies|Skewer and grill or bake|Serve with chutney",
                    prep_time="25 mins",
                    calories="270 kcal",
                    category="indian",
                    image="/static/images/Paneer-Tikka.webp"
                ),
                Recipe(
                    title="Paneer Butter Masala",
                    ingredients="Paneer,Butter,Cream,Tomatoes,Spices",
                    steps="Cook paneer in butter|Add tomato puree and spices|Simmer with cream|Serve with naan or rice",
                    prep_time="40 mins",
                    calories="450 kcal",
                    category="indian",
                    image="/static/images/Paneer-Butter-Masala.webp"
                ),
                Recipe(
                    title="Chicken Biryani",
                    ingredients="Rice,Chicken,Spices,Onions,Yogurt",
                    steps="Marinate chicken|Cook partially rice|Layer rice and chicken|Cook on low heat",
                    prep_time="1 hr",
                    calories="600 kcal",
                    category="indian",
                    image="/static/images/biriyani.jpg"
                ),

                # Breakfast Recipes
                Recipe(
                    title="Pancakes",
                    ingredients="Flour,Eggs,Milk,Sugar,Baking powder",
                    steps="Mix ingredients|Cook on a hot griddle|Serve with syrup and butter",
                    prep_time="20 mins",
                    calories="300 kcal",
                    category="breakfast",
                    image="/static/images/Pancakes.jpg"
                ),
                Recipe(
                    title="Scrambled Eggs",
                    ingredients="Eggs,Butter,Salt,Pepper",
                    steps="Whisk eggs|Cook in a pan with butter|Season with salt and pepper",
                    prep_time="5 mins",
                    calories="200 kcal",
                    category="breakfast",
                    image="/static/images/Scrambled-Eggs.jpg"
                ),
                Recipe(
                    title="French Toast",
                    ingredients="Bread,Eggs,Milk,Cinnamon,Sugar",
                    steps="Dip bread in egg mixture|Cook in a pan until golden|Serve with syrup",
                    prep_time="15 mins",
                    calories="250 kcal",
                    category="breakfast",
                    image="/static/images/French-Toast.jpg"
                ),
                Recipe(
                    title="Oatmeal",
                    ingredients="Oats,Milk,Honey,Fruit",
                    steps="Cook oats in milk|Add honey and fruit",
                    prep_time="10 mins",
                    calories="180 kcal",
                    category="breakfast",
                    image="/static/images/Oatmeal.webp"
                ),
                Recipe(
                    title="Smoothie",
                    ingredients="Banana,Strawberries,Yogurt,Honey",
                    steps="Blend all ingredients together|Serve cold",
                    prep_time="5 mins",
                    calories="150 kcal",
                    category="breakfast",
                    image="/static/images/Smoothie.jpg"
                )
            ]
            db.session.bulk_save_objects(sample_recipes)
            db.session.commit()

@app.route('/search', methods=['GET'])
def search_recipes():
    search_term = request.args.get('q', '').lower()
    category = request.args.get('category', '')
    max_time = request.args.get('max_time', '0')
    if not search_term:
        return jsonify({"error": "Please enter a search term"}), 400

    try:
        max_time = int(max_time.replace(' mins', '').replace(' hr', '60'))
    except ValueError:
        max_time = 0
    
    query = Recipe.query
    
    if search_term:
        query = query.filter(
            db.or_(
                Recipe.title.ilike(f'%{search_term}%'),
                Recipe.ingredients.ilike(f'%{search_term}%')
            )
        )
    
    if category:
        query = query.filter_by(category=category)
    
    if max_time > 0:
        # Convert all times to minutes for comparison
        query = query.filter(db.cast(db.substr(Recipe.prep_time, 1, 2), db.Integer) <= max_time)
    
    recipes = [recipe.to_dict() for recipe in query.all()]
    return jsonify(recipes)










# Routes
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard.html'))
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if not username or not email or not password or not confirm_password:
            flash('All fields are required!', 'error')
        elif password != confirm_password:
            flash('Passwords do not match!', 'error')
        else:
            conn = get_db_connection()
            existing_user = conn.execute('SELECT * FROM users WHERE username = ? OR email = ?', 
                                       (username, email)).fetchone()
            if existing_user:
                flash('Username or email already exists!', 'error')
            else:
                hashed_password = generate_password_hash(password)
                conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                           (username, email, hashed_password))
                conn.commit()
                conn.close()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash('Please fill in all fields!', 'error')
        else:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            conn.close()
            
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password!', 'error')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/indian')
def indian():
    return render_template('indian.html')

@app.route('/chinese')
def chinese():
    return render_template('chinese.html')

@app.route('/mexican')
def mexican():
    return render_template('mexican.html')

@app.route('/italy')
def italy():
    return render_template('italy.html')

@app.route('/recipes')
def recipes():
    return render_template('recipes.html')

@app.route('/breakfast')
def breakfast():
    return render_template('breakfast.html')

@app.route('/lunch')
def lunch():
    return render_template('lunch.html')

@app.route('/dinner')
def dinner():
    return render_template('dinner.html')




if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)