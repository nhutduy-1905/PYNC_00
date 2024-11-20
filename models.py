from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, func, UUID
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)

class AuthToken(db.Model):
    __tablename__ = 'auth_token'
    id = Column(Integer, primary_key=True)
    token = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    token_expires = Column(DateTime, server_default=func.now(), nullable=False)

class Product(db.Model):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    image_path = Column(String(255))

class ProductInShoppingCart(db.Model):
    __tablename__ = 'product_in_shopping_cart'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)

class Purchase(db.Model):
    __tablename__ = 'purchase'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    city = Column(String(255), nullable=False)
    street_address = Column(String(255), nullable=False)
    state = Column(String(255), nullable=False)
    post_code = Column(String(20), nullable=False)
    country = Column(String(255), nullable=False)

class ProductInPurchase(db.Model):
    __tablename__ = 'product_in_purchase'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    purchase_id = Column(Integer, ForeignKey('purchase.id'), nullable=False)