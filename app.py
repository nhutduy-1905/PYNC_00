from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
import os
import bcrypt
import uuid

load_dotenv()

tmp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app = Flask('ecommerce', static_url_path='', template_folder=tmp_dir,
   static_folder=static_folder)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db, Customer, AuthToken, Product, ProductInShoppingCart, Purchase, ProductInPurchase

db.init_app(app)

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/api/user/signup', methods=['POST'])
def signup():
    data = request.get_json()
    password = data['password']
    salt = bcrypt.gensalt()
    encrypted_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    new_customer = Customer(
        username=data['username'],
        email=data['email'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        password=encrypted_password
    )
    db.session.add(new_customer)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return "Username or Email already exists", 400
    return jsonify({"message": "User created successfully"}), 201

@app.route('/api/user/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    customer = Customer.query.filter_by(username=username).first()
    if customer and bcrypt.checkpw(password.encode('utf-8'), customer.password.encode('utf-8')):
        auth_token = AuthToken(customer_id=customer.id)
        db.session.add(auth_token)
        db.session.commit()
        return jsonify({"auth_token": str(auth_token.token), "customer_id": customer.id}), 200
    return "Invalid username or password", 401

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name, "price": str(p.price), "image_path": p.image_path} for p in products])

@app.route('/api/product/<int:prod_id>', methods=['GET'])
def get_product(prod_id):
    product = Product.query.get_or_404(prod_id)
    return jsonify({"id": product.id, "name": product.name, "price": str(product.price), "image_path": product.image_path})

@app.route('/api/shopping_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    auth_token = data.get('auth_token')
    product_id = data.get('product_id')
    token = AuthToken.query.filter_by(token=auth_token).first()
    if not token:
        return "Invalid token", 403
    new_item = ProductInShoppingCart(product_id=product_id, customer_id=token.customer_id)
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Product added to cart"}), 201

@app.route('/api/shopping_cart', methods=['GET'])
def view_cart():
    auth_token = request.args.get('auth_token')
    token = AuthToken.query.filter_by(token=auth_token).first()
    if not token:
        return "Invalid token", 403
    
    cart_items = ProductInShoppingCart.query.filter_by(customer_id=token.customer_id).all()
    products = Product.query.filter(Product.id.in_([item.product_id for item in cart_items])).all()
    total_price = sum([p.price for p in products])
    cart_details = [{
        "item_id": item.id,
        "product_id": p.id,
        "name": p.name,
        "price": str(p.price),
        "image_path": p.image_path
    } for item in cart_items for p in products if item.product_id == p.id]
    return jsonify({"total_price": total_price, "product_query": cart_details})

@app.route('/api/shopping_cart/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    auth_token = data.get('auth_token')
    token = AuthToken.query.filter_by(token=auth_token).first()
    if not token:
        return "Invalid token", 403
    cart_items = ProductInShoppingCart.query.filter_by(customer_id=token.customer_id).all()
    total_price = sum([item.product.price for item in cart_items])
    new_purchase = Purchase(
        customer_id=token.customer_id,
        total_price=total_price,
        city=data['city'],
        street_address=data['street_address'],
        state=data['state'],
        post_code=data['post_code'],
        country=data['country']
    )
    db.session.add(new_purchase)
    db.session.commit()
    for item in cart_items:
        db.session.add(ProductInPurchase(product_id=item.product_id, purchase_id=new_purchase.id))
        db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Checkout successful", "purchase_id": new_purchase.id}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)