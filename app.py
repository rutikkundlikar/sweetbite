from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "sweetbite_secret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sweetbite.db'
db = SQLAlchemy(app)

# Database Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    image = db.Column(db.String(200))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

@app.route('/')
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)

@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    if "user_id" not in session:
        return redirect("/login")

    new_item = Cart(user_id=session["user_id"], product_id=id)
    db.session.add(new_item)
    db.session.commit()
    return redirect('/cart')

@app.route('/cart')
def cart():
    if "user_id" not in session:
        return redirect("/login")

    items = Cart.query.filter_by(user_id=session["user_id"]).all()
    return render_template("cart.html", items=items)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form["email"]

        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email)
            db.session.add(user)
            db.session.commit()

        session["user_id"] = user.id
        return redirect('/')

    return render_template("login.html")

# ADMIN
@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == "POST":
        name = request.form['name']
        price = request.form['price']
        image = request.form['image']

        product = Product(name=name, price=price, image=image)
        db.session.add(product)
        db.session.commit()

    products = Product.query.all()
    return render_template("admin_dashboard.html", products=products)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
